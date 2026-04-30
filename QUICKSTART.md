[QUICKSTART.md](https://github.com/user-attachments/files/27247299/QUICKSTART.md)
# GenRoute AI - Quick Start Guide## Project OverviewGenRoute AI is an advanced transaction routing system that leverages AI to optimize cryptocurrency transactions across multiple blockchains and protocols. This guide provides step-by-step instructions for setting up and running the project locally.## Prerequisites- Node.js (v18 or higher)- Python (v3.8 or higher)- Git- Docker (optional, for containerized deployment)- Blockchain development tools (Hardhat, Foundry, etc.)## Installation Steps### 1. Clone the Repository```bashgit clone https://github.com/your-org/genroute-ai.gitcd genroute-ai
2. Install Backend Dependencies
bash
12
cd backendpip install -r requirements.txt
3. Install Frontend Dependencies
bash
12
cd ../frontendnpm install
4. Configure Environment Variables
Create .env files in both backend and frontend directories with the following variables:
Backend (.env):
12345678
NODE_ENV=developmentPORT=3000ALCHEMY_API_KEY=your_alchemy_keyINFURA_PROJECT_ID=your_infura_idPRIVATE_KEY=your_private_keyDATABASE_URL=sqlite:///./genroute.dbJWT_SECRET=your_jwt_secretAI_PROVIDER_API_KEY=your_ai_provider_key
Frontend (.env):
123
VITE_BACKEND_URL=http://localhost:3000VITE_ALCHEMY_API_KEY=your_alchemy_keyVITE_INFURA_PROJECT_ID=your_infura_id
5. Set Up Database
bash
12
cd backendpython -m scripts.setup_db
6. Compile Smart Contracts
bash
12
cd contractsnpx hardhat compile
Running the Application
Development Mode
Start the backend server:
bash
12
cd backendpython -m main
In a new terminal, start the frontend:
bash
12
cd frontendnpm run dev
Production Build
Build the frontend:
bash
12
cd frontendnpm run build
Start the production server:
bash
12
cd backendpython -m main --production
Key Features Setup
AI Transaction Routing
The system automatically analyzes transaction parameters and routes them through optimal paths. To enable this feature, ensure your AI provider API key is correctly configured.
Multi-Chain Support
Configure supported chains in config/chains.json:
json
12345678910
{  "ethereum": {    "rpcUrl": "https://eth-mainnet.alchemyapi.io/v2/...",    "chainId": 1  },  "polygon": {    "rpcUrl": "https://polygon-rpc.com",    "chainId": 137  }}
Security Scanning
Run security tests before deployment:
bash
1
npm run test:security
Testing
Unit Tests
bash
1234567
# Backend testscd backendpytest tests/# Frontend testscd frontendnpm run test
Integration Tests
bash
1
npm run test:integration
API Endpoints
Main Endpoints
POST /api/route: Calculate optimal transaction route
GET /api/status: Check system status
POST /api/simulate: Simulate transaction execution
GET /api/fees: Get current gas fees
Example Usage
bash
12345678
curl -X POST http://localhost:3000/api/route \  -H "Content-Type: application/json" \  -d '{    "from": "0x...",    "to": "0x...",    "amount": "1.0",    "token": "ETH"  }'
Troubleshooting
Common Issues
Port Already in Use: Change PORT variable in .env file
API Keys Not Working: Verify API keys in environment variables
Database Connection Error: Ensure database service is running
Getting Help
Check the full documentation
Join our Discord community
Create an issue on GitHub
Next Steps
Review the architecture documentation
Explore the API reference
Configure your preferred blockchain networks
Set up monitoring and logging
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354
