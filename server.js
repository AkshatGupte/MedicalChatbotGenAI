const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Keep Python process alive
let pythonProcess = null;
let isPythonReady = false;

// Initialize Python process
function initializePythonProcess() {
    console.log('Initializing Python process...');
    pythonProcess = spawn('python', ['chatbot_wrapper.py']);
    
    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output.includes('ready')) {
            console.log('Python process is ready!');
            isPythonReady = true;
        }
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.log('Python stderr:', data.toString());
    });
    
    pythonProcess.on('close', (code) => {
        console.log('Python process closed with code:', code);
        isPythonReady = false;
        // Restart process if it crashes
        setTimeout(initializePythonProcess, 1000);
    });
}

// Initialize on startup
initializePythonProcess();

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/chat', async (req, res) => {
    const { message } = req.body;
    
    if (!message) {
        return res.status(400).json({ error: 'Message is required' });
    }
    
    if (!isPythonReady) {
        return res.status(503).json({ 
            error: 'Python process is not ready yet. Please try again in a few seconds.' 
        });
    }
    
    try {
        // Send message to existing Python process
        pythonProcess.stdin.write(message + '\n');
        
        let result = '';
        let responseReceived = false;
        
        const timeout = setTimeout(() => {
            if (!responseReceived) {
                res.status(408).json({ error: 'Request timeout' });
            }
        }, 30000); // 30 second timeout
        
        const dataHandler = (data) => {
            const output = data.toString();
            if (output.includes('{')) {
                try {
                    const response = JSON.parse(output);
                    responseReceived = true;
                    clearTimeout(timeout);
                    res.json(response);
                } catch (e) {
                    // Continue collecting data
                }
            }
        };
        
        pythonProcess.stdout.once('data', dataHandler);
        
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        message: 'Medical chatbot is running',
        pythonReady: isPythonReady
    });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
    console.log('Your existing chain.ipynb logic is ready to process queries!');
    console.log(`Visit http://localhost:${PORT} to use the medical chatbot!`);
});
