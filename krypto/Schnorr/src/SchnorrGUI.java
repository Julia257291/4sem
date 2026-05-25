import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.file.Files;
import java.security.SecureRandom;

public class SchnorrGUI extends JFrame {

    private JTabbedPane tabbedPane;
    private JTextArea messageArea;
    private File selectedFile;

    private JTextField pField;
    private JTextField qField;
    private JTextField hField;

    private JTextField publicKeyField;
    private JTextField s1Field;
    private JTextField s2Field;

    private JLabel fileStatusLabel;

    private Schnorr schnorr;
    private BigInteger currentPublicKey;

    public SchnorrGUI() {
        // Konfiguracja głównego okna
        setTitle("Podpis Cyfrowy - Algorytm Schnorra");
        setSize(850, 750); // Lekko zwiększona szerokość, aby pomieścić nowy przycisk
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(10, 10));

        // --- PANEL GÓRNY: Parametry systemu (p, q, h) ---
        JPanel paramsContainer = new JPanel(new BorderLayout(5, 5));
        paramsContainer.setBorder(BorderFactory.createTitledBorder("Parametry Systemu (p, q, h)"));

        JPanel paramsFields = new JPanel(new GridLayout(3, 2, 5, 5));
        pField = new JTextField();
        qField = new JTextField();
        hField = new JTextField();

        paramsFields.add(new JLabel("p:")); paramsFields.add(pField);
        paramsFields.add(new JLabel("q:")); paramsFields.add(qField);
        paramsFields.add(new JLabel("h:")); paramsFields.add(hField);

        JPanel paramsBtns = new JPanel(new FlowLayout());
        JButton generateParamsBtn = new JButton("Generuj losowe p, q, h");
        JButton applyParamsBtn = new JButton("Zastosuj wpisane p, q, h");

        generateParamsBtn.addActionListener(e -> initializeSchnorr());
        applyParamsBtn.addActionListener(e -> applyCustomParameters());

        paramsBtns.add(generateParamsBtn);
        paramsBtns.add(applyParamsBtn);

        paramsContainer.add(paramsFields, BorderLayout.CENTER);
        paramsContainer.add(paramsBtns, BorderLayout.SOUTH);

        // --- PANEL ŚRODKOWY: Zakładki (Tekst / Plik) ---
        tabbedPane = new JTabbedPane();
        tabbedPane.setBorder(BorderFactory.createTitledBorder("Wiadomość do podpisu/weryfikacji"));

        // Zakładka 1: Tekst
        JPanel textPanel = new JPanel(new BorderLayout(5, 5));
        textPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        messageArea = new JTextArea(8, 50);
        messageArea.setLineWrap(true);
        messageArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(messageArea);
        textPanel.add(new JLabel("Wpisz tekst do podpisania/weryfikacji:"), BorderLayout.NORTH);
        textPanel.add(scrollPane, BorderLayout.CENTER);

        // Zakładka 2: Pliki (PDF, PNG, itp.)
        JPanel filePanel = new JPanel(new BorderLayout(5, 5));
        filePanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        JButton chooseFileBtn = new JButton("Wybierz plik z dysku...");
        chooseFileBtn.addActionListener(e -> selectFileForSigning());

        fileStatusLabel = new JLabel("Nie wybrano żadnego pliku.", SwingConstants.CENTER);
        fileStatusLabel.setForeground(Color.GRAY);

        JPanel fileCenterPanel = new JPanel(new GridLayout(2, 1, 10, 10));
        fileCenterPanel.add(chooseFileBtn);
        fileCenterPanel.add(fileStatusLabel);

        filePanel.add(new JLabel("Wybierz plik (np. PDF, PNG) do podpisania/weryfikacji:"), BorderLayout.NORTH);
        filePanel.add(fileCenterPanel, BorderLayout.CENTER);

        tabbedPane.addTab("Podpis Tekstu", textPanel);
        tabbedPane.addTab("Podpis Pliku", filePanel);

        // --- PANEL DOLNY: Przyciski akcji i wyniki ---
        JPanel bottomContainer = new JPanel(new BorderLayout(5, 5));

        JPanel actionPanel = new JPanel(new FlowLayout());
        JButton signBtn = new JButton("Generuj Podpis");
        JButton verifyBtn = new JButton("Weryfikuj Podpis");
        JButton saveBtn = new JButton("Zapisz do pliku");
        JButton loadBtn = new JButton("Wczytaj z pliku"); // <-- NOWY PRZYCISK

        signBtn.addActionListener(e -> signAction());
        verifyBtn.addActionListener(e -> verifyAction());
        saveBtn.addActionListener(e -> saveParametersAndSignature());
        loadBtn.addActionListener(e -> loadParametersAndSignature()); // <-- AKCJA DLA NOWEGO PRZYCISKU

        actionPanel.add(signBtn);
        actionPanel.add(verifyBtn);
        actionPanel.add(saveBtn);
        actionPanel.add(loadBtn); // <-- DODANIE DO PANELU

        JPanel resultsPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        resultsPanel.setBorder(BorderFactory.createTitledBorder("Klucz Publiczny i Podpis"));

        resultsPanel.add(new JLabel("Klucz publiczny (v):"));
        publicKeyField = new JTextField();
        resultsPanel.add(publicKeyField);

        resultsPanel.add(new JLabel("Podpis (s1):"));
        s1Field = new JTextField();
        resultsPanel.add(s1Field);

        resultsPanel.add(new JLabel("Podpis (s2):"));
        s2Field = new JTextField();
        resultsPanel.add(s2Field);

        bottomContainer.add(actionPanel, BorderLayout.NORTH);
        bottomContainer.add(resultsPanel, BorderLayout.CENTER);

        // Dodanie głównych kontenerów do okna
        add(paramsContainer, BorderLayout.NORTH);
        add(tabbedPane, BorderLayout.CENTER);
        add(bottomContainer, BorderLayout.SOUTH);
    }

    private void initializeSchnorr() {
        try {
            SecureRandom random = new SecureRandom();
            BigInteger q = BigInteger.probablePrime(160, random);
            BigInteger p;
            BigInteger multiplier;

            do {
                multiplier = new BigInteger(352, random);
                p = q.multiply(multiplier).add(BigInteger.ONE);
            } while (!p.isProbablePrime(100));

            BigInteger h;
            do {
                BigInteger g = new BigInteger(p.bitLength() - 1, random).add(BigInteger.TWO);
                h = g.modPow(multiplier, p);
            } while (h.equals(BigInteger.ONE));

            schnorr = new Schnorr(p, q, h);
            currentPublicKey = null;

            pField.setText(p.toString()); pField.setCaretPosition(0);
            qField.setText(q.toString()); qField.setCaretPosition(0);
            hField.setText(h.toString()); hField.setCaretPosition(0);
            publicKeyField.setText("");
            s1Field.setText("");
            s2Field.setText("");

        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Błąd podczas generowania parametrów: " + e.getMessage());
        }
    }

    private void applyCustomParameters() {
        try {
            String pStr = pField.getText().trim();
            String qStr = qField.getText().trim();
            String hStr = hField.getText().trim();

            if (pStr.isEmpty() || qStr.isEmpty() || hStr.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Pola p, q, h nie mogą być puste!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                return;
            }

            BigInteger p = new BigInteger(pStr);
            BigInteger q = new BigInteger(qStr);
            BigInteger h = new BigInteger(hStr);

            schnorr = new Schnorr(p, q, h);
            currentPublicKey = null;

            pField.setText(p.toString()); pField.setCaretPosition(0);
            qField.setText(q.toString()); qField.setCaretPosition(0);
            hField.setText(h.toString()); hField.setCaretPosition(0);
            publicKeyField.setText("");
            s1Field.setText("");
            s2Field.setText("");

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Parametry p, q, h muszą być poprawnymi liczbami całkowitymi!", "Błąd formatu", JOptionPane.ERROR_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Wystąpił błąd podczas ustawiania parametrów: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void selectFileForSigning() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            selectedFile = fileChooser.getSelectedFile();
            fileStatusLabel.setText("Wybrany plik: " + selectedFile.getAbsolutePath());
            fileStatusLabel.setForeground(new Color(0, 128, 0));
        }
    }

    private void signAction() {
        try {
            BigInteger[] signature;
            currentPublicKey = schnorr.generatePublicKey();
            if (tabbedPane.getSelectedIndex() == 0) {
                String message = messageArea.getText();
                if (message.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "Wiadomość nie może być pusta!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                signature = schnorr.generateSignature(message);
            } else {
                if (selectedFile == null || !selectedFile.exists()) {
                    JOptionPane.showMessageDialog(this, "Wybierz poprawny plik!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                byte[] fileBytes = Files.readAllBytes(selectedFile.toPath());
                signature = schnorr.generateSignature(fileBytes);
            }

            publicKeyField.setText(currentPublicKey.toString());
            publicKeyField.setCaretPosition(0);
            s1Field.setText(signature[0].toString());
            s1Field.setCaretPosition(0);
            s2Field.setText(signature[1].toString());
            s2Field.setCaretPosition(0);

        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Błąd odczytu pliku: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Błąd podpisania: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void verifyAction() {
        String vStr = publicKeyField.getText().trim();
        String s1Str = s1Field.getText().trim();
        String s2Str = s2Field.getText().trim();

        if (vStr.isEmpty() || s1Str.isEmpty() || s2Str.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Wypełnij klucz publiczny (v) oraz oba pola podpisu (s1, s2).", "Brak danych", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            BigInteger v = new BigInteger(vStr);
            BigInteger s1 = new BigInteger(s1Str);
            BigInteger s2 = new BigInteger(s2Str);
            BigInteger[] signature = new BigInteger[]{s1, s2};

            boolean isValid = false;

            if (tabbedPane.getSelectedIndex() == 0) {
                String message = messageArea.getText();
                if (message.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "Wiadomość tekstowa jest pusta!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                isValid = schnorr.verifySignature(message, signature, v);
            } else {
                if (selectedFile == null || !selectedFile.exists()) {
                    JOptionPane.showMessageDialog(this, "Wybierz poprawny plik do weryfikacji!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                byte[] fileBytes = Files.readAllBytes(selectedFile.toPath());
                isValid = schnorr.verifySignature(fileBytes, signature, v);
            }

            if (isValid) {
                JOptionPane.showMessageDialog(this, "Podpis jest prawidłowy!", "Sukces", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Podpis jest NIEPRAWIDŁOWY!", "Błąd weryfikacji", JOptionPane.ERROR_MESSAGE);
            }

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Pola v, s1 i s2 muszą zawierać poprawne liczby całkowite!", "Błąd formatu", JOptionPane.ERROR_MESSAGE);
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Błąd odczytu pliku: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Błąd weryfikacji: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void saveParametersAndSignature() {
        if (pField.getText().isEmpty() || s1Field.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Brak danych do zapisania! Wygeneruj najpierw parametry i podpis.", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
            return;
        }

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Zapisz parametry i podpis");
        fileChooser.setSelectedFile(new File("schnorr_data.txt"));

        int userSelection = fileChooser.showSaveDialog(this);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToSave = fileChooser.getSelectedFile();

            try (java.io.PrintWriter writer = new java.io.PrintWriter(fileToSave)) {
                writer.println(pField.getText().trim());
                writer.println(qField.getText().trim());
                writer.println(hField.getText().trim());
                writer.println(publicKeyField.getText().trim());
                writer.println(s1Field.getText().trim());
                writer.println(s2Field.getText().trim());

                JOptionPane.showMessageDialog(this, "Dane zostały pomyślnie zapisane do pliku!", "Sukces", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Błąd podczas zapisu do pliku: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    // --- NOWA METODA: Wczytywanie danych analogiczne do zapisu ---
    private void loadParametersAndSignature() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Wczytaj parametry i podpis");

        int userSelection = fileChooser.showOpenDialog(this);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToLoad = fileChooser.getSelectedFile();

            try (BufferedReader reader = new BufferedReader(new FileReader(fileToLoad))) {
                String pStr = reader.readLine();
                String qStr = reader.readLine();
                String hStr = reader.readLine();
                String vStr = reader.readLine();
                String s1Str = reader.readLine();
                String s2Str = reader.readLine();

                // Sprawdzenie czy plik zawiera wystarczającą liczbę linii
                if (pStr == null || qStr == null || hStr == null || vStr == null || s1Str == null || s2Str == null) {
                    JOptionPane.showMessageDialog(this, "Plik ma nieprawidłowy format lub jest uszkodzony!", "Błąd struktury pliku", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                // Parsowanie i inicjalizacja obiektu Schnorr
                BigInteger p = new BigInteger(pStr.trim());
                BigInteger q = new BigInteger(qStr.trim());
                BigInteger h = new BigInteger(hStr.trim());

                schnorr = new Schnorr(p, q, h);
                currentPublicKey = new BigInteger(vStr.trim());

                // Uaktualnienie pól tekstowych w GUI
                pField.setText(pStr.trim()); pField.setCaretPosition(0);
                qField.setText(qStr.trim()); qField.setCaretPosition(0);
                hField.setText(hStr.trim()); hField.setCaretPosition(0);

                publicKeyField.setText(vStr.trim()); publicKeyField.setCaretPosition(0);
                s1Field.setText(s1Str.trim()); s1Field.setCaretPosition(0);
                s2Field.setText(s2Str.trim()); s2Field.setCaretPosition(0);

                JOptionPane.showMessageDialog(this, "Dane zostały pomyślnie wczytane z pliku!", "Sukces", JOptionPane.INFORMATION_MESSAGE);

            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Wczytywane dane muszą być poprawnymi liczbami całkowitymi!", "Błąd formatu", JOptionPane.ERROR_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Błąd podczas odczytu z pliku: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}

            SchnorrGUI app = new SchnorrGUI();
            app.setVisible(true);
        });
    }
}