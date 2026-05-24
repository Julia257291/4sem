import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.MessageDigest;

public class Schnorr {
    //--Te trzy parametry są podawane do publicznej wiadomości --
    public BigInteger p; //używana jako mod p
    public BigInteger q; //q > 2^140
    public BigInteger h; // nierówne 1, h^q = 1 mod p

    private SecureRandom randomNum;
    private BigInteger a; //klucz prywatny, liczba 1 < a < p-1

    public Schnorr(BigInteger p, BigInteger q, BigInteger h){
        this.p = p;
        this.q = q;
        this.h = h;
        this.randomNum = new SecureRandom();
        this.a = generateSecureRandom(q);
    }

    private BigInteger generateSecureRandom(BigInteger limit) {
        if (this.randomNum == null) {
            this.randomNum = new SecureRandom();
        }
        BigInteger random;
        do {
            random = new BigInteger(limit.bitLength(), randomNum);
        } while (random.compareTo(BigInteger.ONE) <= 0 || random.compareTo(limit) >= 0);

        return random;
    }

    public BigInteger generatePublicKey(){
        //h^a
        BigInteger num = h.modPow(a, p);
        BigInteger v = num.modInverse(p);
        return v; //Public key v =(h^a)^-1 mod p
    }

    private byte[] concatenate(BigInteger M, BigInteger X) {
        byte[] mBytes = M.toByteArray();
        byte[] xBytes = X.toByteArray();
        byte[] combined = new byte[mBytes.length + xBytes.length];
        System.arraycopy(mBytes, 0, combined, 0, mBytes.length);
        System.arraycopy(xBytes, 0, combined, mBytes.length, xBytes.length);
        return combined;
    }

    // GŁÓWNA METODA PODPISUJĄCA (Dla dowolnych bajtów - np. plików)
    public BigInteger[] generateSignature(byte[] messageBytes) throws NoSuchAlgorithmException {
        BigInteger M = new BigInteger(1, messageBytes);
        BigInteger r = generateSecureRandom(q); //generowanie random r
        BigInteger X = h.modPow(r, p); //commitment  h^r mod p
        byte[] combined = concatenate(M, X); //konkatenacja MX
        MessageDigest hashAlgorithm = MessageDigest.getInstance("SHA-256");
        byte[] hash = hashAlgorithm.digest(combined); //hashowanie f(MX)
        BigInteger s1 = new BigInteger(1, hash); //żeby dało się wyliczyć s2, zawsze dodatnia
        BigInteger s2 = r.add(a.multiply(s1)).mod(q); //s2 = (r +as1) mod q
        return new BigInteger[] { s1, s2 };
    }

    // METODA POMOCNICZA DLA TEKSTU
    public BigInteger[] generateSignature(String message) throws NoSuchAlgorithmException {
        byte[] messageBytes = message.getBytes(StandardCharsets.UTF_8);
        return generateSignature(messageBytes);
    }

    // GŁÓWNA METODA WERYFIKUJĄCA (Dla dowolnych bajtów - np. plików)
    public boolean verifySignature(byte[] messageBytes, BigInteger[] signature, BigInteger v) throws NoSuchAlgorithmException {
        BigInteger M = new BigInteger(1, messageBytes);
        BigInteger s1 = signature[0];
        BigInteger s2 = signature[1];
        // Z = (h^s2 * v^s1) mod p
        BigInteger part1 = h.modPow(s2, p); //h^s2
        BigInteger part2 = v.modPow(s1, p); //v^s1
        BigInteger Z = part1.multiply(part2).mod(p);
        // Ponowne hashowanie M i Z
        byte[] combined = concatenate(M, Z);
        MessageDigest hashAlgorithm = MessageDigest.getInstance("SHA-256");
        byte[] expectedHash = hashAlgorithm.digest(combined);
        BigInteger expectedS1 = new BigInteger(1, expectedHash);
        return expectedS1.equals(s1); //prawda jeśli są sobie równe
    }

    // METODA POMOCNICZA DLA TEKSTU
    public boolean verifySignature(String message, BigInteger[] signature, BigInteger v) throws NoSuchAlgorithmException {
        return verifySignature(message.getBytes(StandardCharsets.UTF_8), signature, v);
    }
}