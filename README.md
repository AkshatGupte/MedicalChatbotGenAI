# Medical Chatbot - React + Express + LangChain

A medical chatbot built with React frontend, Express backend, and your existing LangChain logic from `chain.ipynb`.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP    ┌─────────────────┐    Child Process    ┌─────────────────┐
│   React.js      │ ──────────→ │   Express.js    │ ──────────────→    │   Python        │
│   Frontend      │             │   Backend       │                    │   (Your Chain)  │
│                 │ ←────────── │                 │ ←───────────────── │                 │
└─────────────────┘             └─────────────────┘                    └─────────────────┘
```

## 📁 Project Structure

```
MedicalChatbot/
├── chain.ipynb                    # Your existing notebook (unchanged)
├── chatbot.ipynb                  # Your existing notebook (unchanged)
├── chain_logic.py                 # Extracted chain.ipynb logic
├── chatbot_wrapper.py             # Python wrapper for Express
├── server.js                      # Express backend server
├── package.json                   # Backend dependencies
├── src/
│   ├── App.js                     # React frontend component
│   ├── App.css                    # Frontend styling
│   └── package.json               # Frontend dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ with your existing environment
- Node.js 16+ and npm
- Your existing `.env` file with API keys

### Step 1: Install Backend Dependencies
```bash
npm install
```

### Step 2: Install Frontend Dependencies
```bash
cd src
npm install
cd ..
```

### Step 3: Verify Environment Variables
Make sure your `.env` file contains:
```
PINECONE_API_KEY=your_pinecone_api_key
HUGGINGFACE_ACCESS_TOKEN=your_huggingface_token
```

## 🏃‍♂️ Running the Application

### Start the Backend (Express Server)
```bash
# Terminal 1
npm start
# or for development with auto-restart
npm run dev
```

The backend will start on `http://localhost:3001`

### Start the Frontend (React App)
```bash
# Terminal 2
cd src
npm start
```

The frontend will start on `http://localhost:3000`

## 🔧 How It Works

1. **User types a medical question** in the React chat interface
2. **React sends HTTP POST request** to Express backend
3. **Express spawns Python process** and calls your existing chain logic
4. **Your chain.ipynb logic runs**:
   - Searches Pinecone vector store for relevant medical documents
   - Retrieves context using your retriever
   - Processes through your LangChain pipeline
   - Generates response using HuggingFace LLM
5. **Response returns** through the same path back to React
6. **User sees medical answer** in the chat interface

## 🎯 Key Features

- ✅ **No changes to your existing Python code**
- ✅ **Modern React chat interface**
- ✅ **Real-time medical responses**
- ✅ **Responsive design for mobile/desktop**
- ✅ **Loading states and error handling**
- ✅ **Professional medical-themed UI**

## 🛠️ Customization

### Backend Configuration
- Modify `server.js` to change API endpoints
- Adjust port numbers in `server.js`

### Frontend Styling
- Edit `src/App.css` for custom styling
- Modify `src/App.js` for UI changes

### Python Logic
- Your existing `chain.ipynb` logic remains unchanged
- Modify `chain_logic.py` if you want to update the chain

## 🐛 Troubleshooting

### Common Issues

1. **Python process fails**
   - Check your `.env` file has correct API keys
   - Verify all Python dependencies are installed
   - Check Python path in `server.js`

2. **Frontend can't connect to backend**
   - Ensure backend is running on port 3001
   - Check CORS settings in `server.js`
   - Verify the API endpoint URL in `src/App.js`

3. **Import errors in Python**
   - Make sure all LangChain dependencies are installed
   - Check Python environment activation

### Debug Mode
```bash
# Backend with detailed logging
DEBUG=* npm start

# Frontend with React dev tools
cd src && npm start
```

## 📝 API Endpoints

- `POST /chat` - Send medical query and get response
- `GET /health` - Health check endpoint

### Request Format
```json
{
  "message": "What causes cardiac arrest?"
}
```

### Response Format
```json
{
  "response": "Cardiac arrest is caused by...",
  "status": "success"
}
```

## 🔒 Security Notes

- API keys are stored in `.env` file (backend only)
- CORS is enabled for development
- Input validation is handled in Express
- Error handling prevents sensitive data exposure

## 🚀 Deployment

### Backend Deployment
- Deploy to Railway, Render, or AWS
- Set environment variables in deployment platform
- Ensure Python dependencies are available

### Frontend Deployment
- Build with `cd src && npm run build`
- Deploy to Vercel, Netlify, or similar
- Update API endpoint URL for production

## 📞 Support

Your existing LangChain medical chatbot logic is now accessible through a modern web interface! The integration preserves all your existing functionality while adding a beautiful React frontend.
