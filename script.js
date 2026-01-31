/* Fixed Imports to prevent dependency conflicts and ensure latest versions */
import { EditorView, basicSetup } from "https://esm.sh/codemirror";
import { cpp } from "https://esm.sh/@codemirror/lang-cpp";
import { oneDark } from "https://esm.sh/@codemirror/theme-one-dark";

console.log("KhelKhatam IDE: Script Loaded");

// DOM Elements
const runBtn = document.getElementById('runBtn');
const terminalOutput = document.getElementById('terminal-output');
const clearTermBtn = document.getElementById('clearTerm');

// Initial KhelKhatam Code
const initialCode = `// Write your KhelKhatam code here
shuru_kar
    bol "Hello World"
bas_khatam
`;

// Initialize Left Editor (KhelKhatam - Plain Text for now as no lexer exists in CM)
const inputEditor = new EditorView({
    doc: initialCode,
    extensions: [
        basicSetup, // Includes defaultKeymap, history, etc.
        oneDark,
        EditorView.lineWrapping
    ],
    parent: document.getElementById('editor-container')
});

// Initialize Right Editor (C++ Viewer - Read Only)
const cppViewer = new EditorView({
    doc: "// C++ Output will appear here...",
    extensions: [
        basicSetup,
        cpp(),
        oneDark,
        EditorView.editable.of(false), // Read-only
        EditorView.lineWrapping
    ],
    parent: document.getElementById('cpp-container')
});

// Logging helper
function logToTerminal(msg, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    let colorClass = 'text-gray-300';
    if (type === 'error') colorClass = 'text-red-400';
    if (type === 'success') colorClass = 'text-green-400';

    // Create new element (safer than innerHTML appends for large logs)
    const line = document.createElement('div');
    line.className = `${colorClass} mb-1`;
    line.textContent = `[${timestamp}] ${msg}`;

    terminalOutput.appendChild(line);
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

// Clear Terminal
clearTermBtn.addEventListener('click', () => {
    terminalOutput.innerHTML = '';
});

// Run Button Logic
const originalBtnContent = runBtn.innerHTML;

runBtn.addEventListener('click', async (e) => {
    // Prevent default form submission
    e.preventDefault();

    const code = inputEditor.state.doc.toString();

    // UI Feedback
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
            // Update C++ Viewer (Replacing entire document)
            const transaction = cppViewer.state.update({
                changes: { from: 0, to: cppViewer.state.doc.length, insert: result.cpp }
            });
            cppViewer.dispatch(transaction);

            // Append Output to Terminal
            logToTerminal('Compilation & Execution Finished:', 'success');

            const outputDiv = document.createElement('div');
            // Ensure whitespace is preserved
            outputDiv.className = 'text-white pl-4 border-l-2 border-gray-600 mt-2 mb-4 whitespace-pre-wrap font-mono';
            // Data Mapping: result.output matches app.py JSON key
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
        // Reset Button to Original State
        runBtn.disabled = false;
        runBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        runBtn.innerHTML = originalBtnContent;
    }
});
