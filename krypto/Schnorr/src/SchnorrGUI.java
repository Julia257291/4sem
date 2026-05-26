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

    private JRadioButton signTextRadio;
    private JRadioButton signFileRadio;

    private JTextField pField;
    private JTextField qField;
    private JTextField hField;
    private JTextField aField;

    private JTextField publicKeyField;
    private JTextField s1Field;
    private JTextField s2Field;

    private JLabel fileStatusLabel;

    private JTabbedPane verifyTabbedPane;
    private JTextArea verifyMessageArea;
    private File verifySelectedFile;
    private JLabel verifyFileStatusLabel;
    private JTextField verifyPField, verifyHField, verifyVField, verifyS1Field, verifyS2Field;

    private Schnorr schnorr;
    private BigInteger currentPublicKey;

    public SchnorrGUI() {
        // Konfiguracja głównego okna
        setTitle("Podpis Cyfrowy - Algorytm Schnorra");
        setSize(850, 750); // Lekko zwiększona szerokość, aby pomieścić nowy przycisk
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        JTabbedPane mainTabs = new JTabbedPane();
        mainTabs.addTab("Konfiguracja i Podpisywanie", SigningTab());
        mainTabs.addTab("Weryfikacja", VerificationTab());
        add(mainTabs);
    }
    private JPanel SigningTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
        // --- PANEL GÓRNY: Parametry systemu (p, q, h) ---
        JPanel paramsContainer = new JPanel(new BorderLayout(5, 5));
        paramsContainer.setBorder(BorderFactory.createTitledBorder("Parametry Systemu (p, q, h)"));

        JPanel paramsFields = new JPanel(new GridLayout(4, 2, 5, 5));
        pField = new JTextField();
        qField = new JTextField();
        hField = new JTextField();
        aField = new JTextField();

        paramsFields.add(new JLabel("p:")); paramsFields.add(pField);
        paramsFields.add(new JLabel("q:")); paramsFields.add(qField);
        paramsFields.add(new JLabel("h:")); paramsFields.add(hField);
        paramsFields.add(new JLabel("Klucz (a):")); paramsFields.add(aField); // Dodanie do panelu

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
        tabbedPane.setBorder(BorderFactory.createTitledBorder("Wiadomość do podpisu"));

        // Zakładka 1: Tekst
        JPanel textPanel = new JPanel(new BorderLayout(5, 5));
        textPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        messageArea = new JTextArea(8, 50);
        messageArea.setLineWrap(true);
        messageArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(messageArea);
        textPanel.add(new JLabel("Wpisz tekst do podpisania:"), BorderLayout.NORTH);
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

        filePanel.add(new JLabel("Wybierz plik (np. PDF, PNG) do podpisania:"), BorderLayout.NORTH);
        filePanel.add(fileCenterPanel, BorderLayout.CENTER);

        tabbedPane.addTab("Podpis Tekstu", textPanel);
        tabbedPane.addTab("Podpis Pliku", filePanel);

        // --- PANEL DOLNY: Przyciski akcji i wyniki ---
        JPanel bottomContainer = new JPanel(new BorderLayout(5, 5));

        JPanel actionPanel = new JPanel(new FlowLayout());
        JButton signBtn = new JButton("Generuj Podpis");
        JButton saveKeysBtn = new JButton("Zapisz swoje klucze");
        JButton exportCertBtn = new JButton("Eksportuj dla odbiorcy");
        JButton loadKeysBtn = new JButton("Wczytaj swoje klucze");

        signBtn.addActionListener(e -> signAction());
        saveKeysBtn.addActionListener(e -> saveMyKeys());
        exportCertBtn.addActionListener(e -> exportCertificate());
        loadKeysBtn.addActionListener(e -> loadMyKeys());

        actionPanel.add(signBtn);
        actionPanel.add(saveKeysBtn);
        actionPanel.add(exportCertBtn);
        actionPanel.add(loadKeysBtn);

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
        panel.add(paramsContainer, BorderLayout.NORTH);
        panel.add(tabbedPane, BorderLayout.CENTER);
        panel.add(bottomContainer, BorderLayout.SOUTH);
        return panel;
    }

    private JPanel VerificationTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        JPanel verifyParamsPanel = new JPanel(new GridLayout(5, 2, 5, 5));
        verifyParamsPanel.setBorder(BorderFactory.createTitledBorder("Dane wymagane do weryfikacji (Brak q oraz a)"));
        verifyPField = new JTextField(); verifyHField = new JTextField(); verifyVField = new JTextField(); verifyS1Field = new JTextField(); verifyS2Field = new JTextField();
        verifyParamsPanel.add(new JLabel("p:")); verifyParamsPanel.add(verifyPField);
        verifyParamsPanel.add(new JLabel("h:")); verifyParamsPanel.add(verifyHField);
        verifyParamsPanel.add(new JLabel("Klucz publiczny (v):")); verifyParamsPanel.add(verifyVField);
        verifyParamsPanel.add(new JLabel("Podpis (s1):")); verifyParamsPanel.add(verifyS1Field);
        verifyParamsPanel.add(new JLabel("Podpis (s2):")); verifyParamsPanel.add(verifyS2Field);

        verifyTabbedPane = new JTabbedPane();
        verifyTabbedPane.setBorder(BorderFactory.createTitledBorder("Weryfikowany dokument"));

        JPanel textPanel = new JPanel(new BorderLayout(5, 5));
        verifyMessageArea = new JTextArea(8, 50); verifyMessageArea.setLineWrap(true);
        textPanel.add(new JLabel("Wpisz sprawdzany tekst:"), BorderLayout.NORTH); textPanel.add(new JScrollPane(verifyMessageArea), BorderLayout.CENTER);

        JPanel filePanel = new JPanel(new BorderLayout(5, 5));
        JButton chooseFileBtn = new JButton("Wybierz plik z dysku...");
        verifyFileStatusLabel = new JLabel("Nie wybrano żadnego pliku.", SwingConstants.CENTER); verifyFileStatusLabel.setForeground(Color.GRAY);
        chooseFileBtn.addActionListener(e -> {
            JFileChooser fc = new JFileChooser();
            if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
                verifySelectedFile = fc.getSelectedFile(); verifyFileStatusLabel.setText(verifySelectedFile.getName());
            }
        });
        JPanel fileCenterPanel = new JPanel(new GridLayout(2, 1, 10, 10));
        fileCenterPanel.add(chooseFileBtn); fileCenterPanel.add(verifyFileStatusLabel);
        filePanel.add(new JLabel("Wybierz sprawdzany plik:"), BorderLayout.NORTH); filePanel.add(fileCenterPanel, BorderLayout.CENTER);

        verifyTabbedPane.addTab("Sprawdź Tekst", textPanel); verifyTabbedPane.addTab("Sprawdź Plik", filePanel);

        // ZMIANA: Zgrupowanie przycisków
        JPanel buttonsPanel = new JPanel(new FlowLayout());

        JButton verifyBtn = new JButton("WERYFIKUJ PODPIS");
        verifyBtn.setFont(new Font("Arial", Font.BOLD, 14));
        verifyBtn.addActionListener(e -> verifyAction());

        JButton loadVerifyBtn = new JButton("Wczytaj certyfikat z pliku");
        loadVerifyBtn.addActionListener(e -> loadVerificationData());

        buttonsPanel.add(verifyBtn);
        buttonsPanel.add(loadVerifyBtn);

        panel.add(verifyParamsPanel, BorderLayout.NORTH);
        panel.add(verifyTabbedPane, BorderLayout.CENTER);
        panel.add(buttonsPanel, BorderLayout.SOUTH);

        return panel;
    }

    private void loadVerificationData() {
        JFileChooser fc = new JFileChooser();
        if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            try (BufferedReader reader = new BufferedReader(new FileReader(fc.getSelectedFile()))) {
                // Odczytujemy dokładnie 5 linijek, które zapisał exportCertificate()
                String pStr = reader.readLine();
                String hStr = reader.readLine();
                String vStr = reader.readLine();
                String s1Str = reader.readLine();
                String s2Str = reader.readLine();

                if (pStr == null || hStr == null || vStr == null || s1Str == null || s2Str == null) {
                    JOptionPane.showMessageDialog(this, "Plik ma nieprawidłowy format lub jest uszkodzony!", "Błąd struktury pliku", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                // Wpisujemy pobrane wartości wprost do okienek weryfikacji
                verifyPField.setText(pStr.trim()); verifyPField.setCaretPosition(0);
                verifyHField.setText(hStr.trim()); verifyHField.setCaretPosition(0);
                verifyVField.setText(vStr.trim()); verifyVField.setCaretPosition(0);
                verifyS1Field.setText(s1Str.trim()); verifyS1Field.setCaretPosition(0);
                verifyS2Field.setText(s2Str.trim()); verifyS2Field.setCaretPosition(0);

                JOptionPane.showMessageDialog(this, "Certyfikat poprawnie wczytany do weryfikacji!");

            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Błąd wczytywania: " + ex.getMessage());
            }
        }
    }

    private void initializeSchnorr() {
        try {
            schnorr = new Schnorr();
            currentPublicKey = schnorr.generatePublicKey();

            pField.setText(schnorr.p.toString()); pField.setCaretPosition(0);
            qField.setText(schnorr.q.toString()); qField.setCaretPosition(0);
            hField.setText(schnorr.h.toString()); hField.setCaretPosition(0);
            aField.setText(schnorr.getPrivateKey().toString()); aField.setCaretPosition(0);
            publicKeyField.setText(""); publicKeyField.setCaretPosition(0);
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
            String aStr = aField.getText().trim();

            if (pStr.isEmpty() || qStr.isEmpty() || hStr.isEmpty() || aStr.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Wszystkie 4 pola muszą być wypełnione!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                return;
            }

            BigInteger p = new BigInteger(pStr);
            BigInteger q = new BigInteger(qStr);
            BigInteger h = new BigInteger(hStr);
            BigInteger a = new BigInteger(aStr);

            schnorr = new Schnorr(p, q, h, a);
            currentPublicKey = schnorr.generatePublicKey();

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
        String pStr = verifyPField.getText().trim();
        String hStr = verifyHField.getText().trim();
        // ZMIANA: używamy zmiennych z zakładki weryfikacji
        String vStr = verifyVField.getText().trim();
        String s1Str = verifyS1Field.getText().trim();
        String s2Str = verifyS2Field.getText().trim();

        if (pStr.isEmpty() || hStr.isEmpty() || vStr.isEmpty() || s1Str.isEmpty() || s2Str.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Wypełnij klucz publiczny (v) oraz oba pola podpisu (s1, s2).", "Brak danych", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            BigInteger p = new BigInteger(pStr);
            BigInteger h = new BigInteger(hStr);
            BigInteger v = new BigInteger(vStr);
            BigInteger s1 = new BigInteger(s1Str);
            BigInteger s2 = new BigInteger(s2Str);
            BigInteger[] signature = new BigInteger[]{s1, s2};

            boolean isValid = false;

            // ZMIANA: tworzymy obiekt tylko do weryfikacji (q i a ustawiamy na 1)
            Schnorr verifier = new Schnorr(p, BigInteger.ONE, h, BigInteger.ONE);

            // ZMIANA: używamy wewnętrznej zakładki weryfikacyjnej i jej pól
            if (verifyTabbedPane.getSelectedIndex() == 0) {
                String message = verifyMessageArea.getText();
                if (message.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "Wiadomość tekstowa jest pusta!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                isValid = verifier.verifySignature(message, signature, v);
            } else {
                if (verifySelectedFile == null || !verifySelectedFile.exists()) {
                    JOptionPane.showMessageDialog(this, "Wybierz poprawny plik do weryfikacji!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
                    return;
                }
                byte[] fileBytes = Files.readAllBytes(verifySelectedFile.toPath());
                isValid = verifier.verifySignature(fileBytes, signature, v);
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

    private void saveMyKeys() {
        if (pField.getText().isEmpty() || aField.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Brak kluczy do zapisania!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
            return;
        }

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Zapisz swoje tajne klucze (p, q, h, a)");
        fileChooser.setSelectedFile(new File("moje_klucze.txt"));

        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try (java.io.PrintWriter writer = new java.io.PrintWriter(fileChooser.getSelectedFile())) {
                writer.println(pField.getText().trim());
                writer.println(qField.getText().trim());
                writer.println(hField.getText().trim());
                writer.println(aField.getText().trim());
                JOptionPane.showMessageDialog(this, "Twoje klucze zostały zapisane pomyślnie!", "Sukces", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Błąd podczas zapisu: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void exportCertificate() {
        if (publicKeyField.getText().isEmpty() || s1Field.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Najpierw wygeneruj podpis!", "Ostrzeżenie", JOptionPane.WARNING_MESSAGE);
            return;
        }

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Eksportuj certyfikat dla weryfikatora");
        fileChooser.setSelectedFile(new File("certyfikat_podpisu.txt"));

        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try (java.io.PrintWriter writer = new java.io.PrintWriter(fileChooser.getSelectedFile())) {
                writer.println(pField.getText().trim());
                writer.println(hField.getText().trim());
                writer.println(publicKeyField.getText().trim());
                writer.println(s1Field.getText().trim());
                writer.println(s2Field.getText().trim());
                JOptionPane.showMessageDialog(this, "Certyfikat (p, h, v, s1, s2) wyeksportowany!", "Sukces", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Błąd podczas eksportu: " + ex.getMessage(), "Błąd", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void loadMyKeys() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Wczytaj swoje klucze");

        if (fileChooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            try (BufferedReader reader = new BufferedReader(new FileReader(fileChooser.getSelectedFile()))) {
                String pStr = reader.readLine();
                String qStr = reader.readLine();
                String hStr = reader.readLine();
                String aStr = reader.readLine();

                if (pStr == null || qStr == null || hStr == null || aStr == null) {
                    JOptionPane.showMessageDialog(this, "Plik ma nieprawidłowy format!", "Błąd struktury pliku", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                BigInteger p = new BigInteger(pStr.trim());
                BigInteger q = new BigInteger(qStr.trim());
                BigInteger h = new BigInteger(hStr.trim());
                BigInteger a = new BigInteger(aStr.trim());

                schnorr = new Schnorr(p, q, h, a);
                currentPublicKey = schnorr.generatePublicKey();

                pField.setText(pStr.trim()); pField.setCaretPosition(0);
                qField.setText(qStr.trim()); qField.setCaretPosition(0);
                hField.setText(hStr.trim()); hField.setCaretPosition(0);
                aField.setText(aStr.trim()); aField.setCaretPosition(0);

                publicKeyField.setText("");
                s1Field.setText("");
                s2Field.setText("");

                JOptionPane.showMessageDialog(this, "Twoje klucze wczytane pomyślnie!", "Sukces", JOptionPane.INFORMATION_MESSAGE);

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
    }}