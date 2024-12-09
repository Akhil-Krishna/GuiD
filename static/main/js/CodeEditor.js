import React, { useState, useEffect } from 'react';
import * as monaco from 'monaco-editor';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

const CodeEditor = ({ questionId }) => {
    const [editor, setEditor] = useState(null);
    const [output, setOutput] = useState('');
    const [correct, setCorrect] = useState(false);

    useEffect(() => {
        if (!editor) {
            const monacoEditor = monaco.editor.create(document.getElementById('editor'), {
                value: '',
                language: 'python',
                theme: 'vs-dark',
            });
            setEditor(monacoEditor);
        }
    }, [editor]);

    const client = new W3CWebSocket('ws://localhost:8000/ws/code/');

    const runCode = () => {
        const code = editor.getValue();
        client.send(JSON.stringify({
            code: code,
            question_id: questionId,
        }));
    };

    client.onmessage = (message) => {
        const data = JSON.parse(message.data);
        setOutput(data.output);
        setCorrect(data.correct);
    };

    return (
        <div>
            <div id="editor" style={{ height: '400px', width: '100%' }}></div>
            <button onClick={runCode}>Run</button>
            <div>
                <h3>Output:</h3>
                <pre>{output}</pre>
                {correct && <p>✅ Correct!</p>}
            </div>
        </div>
    );
};

export default CodeEditor;
