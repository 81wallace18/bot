// whatsapp_handler_node/index.js
const { Client, LocalAuth } = require('whatsapp-web.js');
const axios = require('axios');
const qrcode = require('qrcode-terminal');

// Initialize the WhatsApp client
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true, // Garante que o navegador rode em modo headless
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process', // Isso pode não ser necessário, mas ajuda em alguns ambientes
            '--disable-gpu'
        ],
    }
});

// Generate and display QR code for authentication
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('QR RECEIVED', qr);
});

// Client is ready
client.on('ready', () => {
    console.log('Client is ready!');
});

// Listen for incoming messages
client.on('message', async message => {
    console.log('Message Received:', message.body);

    const user_id = message.from;
    const user_message = message.body;

    try {
        // Send message to Python service
        const pythonServiceUrl = 'http://agent_logic:8000/process-message'; // Replace with your Python service URL if different
        const response = await axios.post(pythonServiceUrl, {
            user_id: user_id,
            message: user_message
        });

        // Process replies from Python service
        const replies = response.data.replies;

        if (replies && Array.isArray(replies)) {
            for (const reply of replies) {
                await client.sendMessage(message.from, reply);
            }
        } else {
            console.error('Invalid response format from Python service:', response.data);
            await client.sendMessage(message.from, 'Desculpe, ocorreu um erro ao processar sua solicitação.');
        }

    } catch (error) {
        console.error('Error communicating with Python service:', error);
        await client.sendMessage(message.from, 'Desculpe, o serviço de processamento está temporariamente indisponível.');
    }
});

// Initialize the client
client.initialize();
