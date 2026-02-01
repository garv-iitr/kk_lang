import { EditorView, basicSetup } from "https://esm.sh/codemirror";
import { autocompletion, snippet } from "https://esm.sh/@codemirror/autocomplete";
import { cpp } from "https://esm.sh/@codemirror/lang-cpp";
import { oneDark } from "https://esm.sh/@codemirror/theme-one-dark";
import { StreamLanguage } from "https://esm.sh/@codemirror/language";
import { tags } from "https://esm.sh/@lezer/highlight";

console.log("KhelKhatam IDE: Script Loaded");

const runBtn = document.getElementById('runBtn');
const terminalOutput = document.getElementById('terminal-output');
const clearTermBtn = document.getElementById('clearTerm');

const initialCode = `// Write your KhelKhatam code here
khel_shuru
    aelaan_karo("khel_khatam")
khel_khatam
`;

const khelKhatamLanguage = StreamLanguage.define({
    token(stream) {
        if (stream.eatSpace()) return null;

        if (stream.match("//")) {
            stream.skipToEnd();
            return "comment";
        }
        if (stream.match('"')) {
            while (!stream.eol()) {
                if (stream.next() == '"' && stream.string[stream.pos - 2] != '\\') {
                    break;
                }
            }
            return "string";
        }

        if (stream.match(/^[0-9]+/)) {
            return "number";
        }
        if (stream.match(/^(shuru_kar|bas_khatam|khel_shuru|khel_khatam|faisla|nahi_toh|khiladi|aelaan_karo|bol)\b/)) {
            return "keyword";
        }

        stream.next();
        return null;
    }
});

function khelKhatamCompletions(context) {
    let word = context.matchBefore(/\w*/);
    if (word.from == word.to && !context.explicit) return null;

    return {
        from: word.from,
        options: [
            { label: "khel_shuru", type: "keyword", info: "Starts the program" },
            { label: "khel_khatam", type: "keyword", info: "Ends the program" },
            { label: "shuru_kar", type: "keyword", info: "Starts the program (legacy)" },
            { label: "bas_khatam", type: "keyword", info: "Ends the program (legacy)" },
            { label: "faisla", type: "keyword", info: "Conditional (if)" },
            { label: "nahi_toh", type: "keyword", info: "Alternative (else)" },
            { label: "khiladi", type: "keyword", info: "Variable declaration" },
            { label: "bol", type: "keyword", info: "Print statement (legacy)" },
            {
                label: "aelaan_karo",
                type: "function",
                apply: snippet('aelaan_karo("${}")'),
                detail: "Print statement"
            }
        ]
    };
}

const inputEditor = new EditorView({
    doc: initialCode,
    extensions: [
        basicSetup,
        khelKhatamLanguage,
        autocompletion({ override: [khelKhatamCompletions] }),
        oneDark,
        EditorView.lineWrapping
    ],
    parent: document.getElementById('editor-container')
});

const cppViewer = new EditorView({
    doc: "// C++ Output will appear here...",
    extensions: [
        basicSetup,
        cpp(),
        oneDark,
        EditorView.editable.of(false),
        EditorView.lineWrapping
    ],
    parent: document.getElementById('cpp-container')
});

function logToTerminal(msg, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    let colorClass = 'text-gray-300';
    if (type === 'error') colorClass = 'text-red-400';
    if (type === 'success') colorClass = 'text-green-400';

    const line = document.createElement('div');
    line.className = `${colorClass} mb-1`;
    line.textContent = `[${timestamp}] ${msg}`;

    terminalOutput.appendChild(line);
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

clearTermBtn.addEventListener('click', () => {
    terminalOutput.innerHTML = '';
});
const originalBtnContent = runBtn.innerHTML;

runBtn.addEventListener('click', async (e) => {
    e.preventDefault();

    const code = inputEditor.state.doc.toString();

    runBtn.disabled = true;
    runBtn.classList.add('opacity-50', 'cursor-not-allowed');
    runBtn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Compiling...`;

    logToTerminal('Sending code to server...', 'info');

    try {
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        const result = await response.json();

        if (response.ok) {
            const transaction = cppViewer.state.update({
                changes: { from: 0, to: cppViewer.state.doc.length, insert: result.cpp }
            });
            cppViewer.dispatch(transaction);

            logToTerminal('Compilation & Execution Finished:', 'success');

            const outputDiv = document.createElement('div');
            outputDiv.className = 'text-white pl-4 border-l-2 border-gray-600 mt-2 mb-4 whitespace-pre-wrap font-mono';
            outputDiv.textContent = result.output;
            terminalOutput.appendChild(outputDiv);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;

        } else {
            logToTerminal(`Server Error: ${result.error}`, 'error');
            if (result.details) {
                const errDiv = document.createElement('div');
                errDiv.className = 'text-red-300 pl-4 border-l-2 border-red-800 mt-1 whitespace-pre-wrap font-mono';
                errDiv.textContent = result.details;
                terminalOutput.appendChild(errDiv);
            }
        }
    } catch (error) {
        logToTerminal(`Network Error: ${error.message}`, 'error');
    } finally {
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        runBtn.innerHTML = originalBtnContent;
    }
});
