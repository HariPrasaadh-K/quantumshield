package com.quantumshield.demo;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.KeyPairGenerator;
import java.security.KeyPair;
import java.security.Signature;
import java.security.MessageDigest;
import java.security.SecureRandom;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

public class CryptoService {

    public byte[] encryptDataWithRSA(byte[] data) throws Exception {
        // RSA Key Generation (Quantum Vulnerable)
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        keyGen.initialize(2048);
        KeyPair keyPair = keyGen.generateKeyPair();

        // RSA Cipher (Key Establishment / Encryption)
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
        return cipher.doFinal(data);
    }

    public byte[] signTransactionWithECDSA(byte[] message) throws Exception {
        // ECDSA Signature Generation (Quantum Vulnerable)
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDSA");
        KeyPair keyPair = keyGen.generateKeyPair();

        Signature signature = Signature.getInstance("SHA256withECDSA");
        signature.initSign(keyPair.getPrivate());
        signature.update(message);
        return signature.sign();
    }

    public byte[] performECDHKeyAgreement() throws Exception {
        // ECDH Key Agreement (Quantum Vulnerable)
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDH");
        KeyPair keyPair = keyGen.generateKeyPair();
        return keyPair.getPublic().getEncoded();
    }

    public byte[] encryptSymmetricAES(byte[] plaintext) throws Exception {
        // AES 256 GCM (Symmetric Encryption - Quantum Resistant with 256-bit key)
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        SecretKey key = keyGen.generateKey();

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(plaintext);
    }

    public byte[] legacyHashMD5(byte[] input) throws Exception {
        // Legacy Weak Hash (Classical Vulnerability)
        MessageDigest md = MessageDigest.getInstance("MD5");
        return md.digest(input);
    }

    public byte[] computeSHA256(byte[] input) throws Exception {
        // Standard Hash
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(input);
    }
}
