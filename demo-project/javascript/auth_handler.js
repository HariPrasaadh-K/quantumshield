const crypto = require('crypto');

function generateKeyPairRSA() {
    // Node.js RSA Key Generation
    const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
        modulusLength: 2048,
    });
    return { publicKey, privateKey };
}

function encryptAESGCM(text, masterKey) {
    // Node.js AES Cipher
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', masterKey, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { encrypted, iv: iv.toString('hex') };
}

function hashMD5(str) {
    // Weak MD5 Hash
    return crypto.createHash('md5').update(str).digest('hex');
}

function hashSHA256(str) {
    // SHA-256 Hash
    return crypto.createHash('sha256').update(str).digest('hex');
}

module.exports = {
    generateKeyPairRSA,
    encryptAESGCM,
    hashMD5,
    hashSHA256
};
