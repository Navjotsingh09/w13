module.exports = async function handler(req, res) {
    // CORS headers so any page on this domain can call this
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    if (req.method !== 'POST') {
        return res.status(405).json({ success: false, message: 'Method not allowed' });
    }

    try {
        const response = await fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'https://w13uk.com',
                'Referer': 'https://w13uk.com/',
            },
            body: JSON.stringify(req.body),
        });
        const data = await response.json();
        return res.status(response.status).json(data);
    } catch (err) {
        return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
    }
};
