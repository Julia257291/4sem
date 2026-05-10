import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.MessageDigest;

public class Schnorr{
    //--Te trzy parametry są podawane do publicznej wiadomości --
    // p i q to liczby pierwsze
    public BigInteger p; //używana jako mod p
    //bardzo duża liczba p > 2^512
    public BigInteger q; //q > 2^140
    public BigInteger h; // nierówne 1, h^q = 1 mod p
    //Trzeba znaleźć takie h, żeby spełniało powyższy warunek
    //Służy jako generator do operacji potęgowania w tym algorytmie

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
            // Tworzymy liczbę o długości bitowej odpowiadającej limitowi
            random = new BigInteger(limit.bitLength(), randomNum);
            // Warunek: 0 < randomNum < limit
            // (ponieważ nasz limit to q, a wzór mówi r <= q-1,
            // to r musi być po prostu mniejsze od q i większe od 0)
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

    public BigInteger[] generateSignature(String message) throws NoSuchAlgorithmException {
        byte[] messageBytes = message.getBytes(StandardCharsets.UTF_8);
        BigInteger M = new BigInteger(1, messageBytes);
        //NoSuchAlgorithmException, żeby nie wyrzucał błędu
        BigInteger r = generateSecureRandom(q); //generowanie random r
        BigInteger X = h.modPow(r, p); //commitment  h^r mod p
        byte[] combined = concatenate(M, X); //konkatenacja MX
        MessageDigest hashAlgorithm = MessageDigest.getInstance("SHA-256");
        byte[] hash = hashAlgorithm.digest(combined); //hashowanie f(MX)
        BigInteger s1 = new BigInteger(1, hash); //żeby dało się wyliczyć s2, zawsze dodatnia
        BigInteger s2 = r.add(a.multiply(s1)).mod(q); //s2 = (r +as1) mod q
        return new BigInteger[] { s1, s2 };
    }

    public boolean verifySignature(String message, BigInteger[] signature, BigInteger v) throws NoSuchAlgorithmException {
        BigInteger M = new BigInteger(1, message.getBytes(StandardCharsets.UTF_8));
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

}