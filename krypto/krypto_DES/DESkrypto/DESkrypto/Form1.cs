using System.Text;
using System.Web;

namespace DESkrypto
{
    public partial class Form1 : Form
    {
        DES des = new DES();
        string? filePathToEncrypt;
        string? filePathToDecrypt;
        public Form1()
        {
            InitializeComponent();
            comboBox1.SelectedIndex = 0;
            panel1.Visible = true;
            panel2.Visible = false;
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox1.SelectedIndex == 0)
            {
                panel1.Visible = true;
                panel2.Visible = false;
            }
            else if (comboBox1.SelectedIndex == 1)
            {
                panel1.Visible = false;
                panel2.Visible = true;
            }
        }

        private void EncryptFileChooseButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                filePathToEncrypt = openFileDialog1.FileName;
                label1.Text = filePathToEncrypt;
            }
        }

        private void DecryptFileChooseButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                filePathToDecrypt = openFileDialog1.FileName;
                label2.Text = filePathToDecrypt;
            }
        }

        private void EncryptButton_Click(object sender, EventArgs e)
        {
            if (!String.IsNullOrEmpty(filePathToEncrypt))
            {
                if (!String.IsNullOrEmpty(textBox4.Text))
                {
                    string outputPath = filePathToEncrypt + ".des";
                    ProcessFile(filePathToEncrypt, outputPath, StringToByteArray(textBox4.Text), true);
                    MessageBox.Show("Zaszyfrowano do:" + outputPath);
                }
                else
                {
                    MessageBox.Show("Wygeneruj lub podaj 8-znakowy klucz szyfrowania");
                }
            }
            else
            {
                MessageBox.Show("Wybierz plik do zaszyfrowania");
            }
        }

        private void DecryptButton_Click(object sender, EventArgs e)
        {
            if (!String.IsNullOrEmpty(filePathToDecrypt))
            {
                if (!String.IsNullOrEmpty(textBox4.Text))
                {
                    if (!filePathToDecrypt.EndsWith(".des"))
                    {
                        MessageBox.Show("Podaj plik z roozszerzeniem .des ");
                    }
                    else
                    {
                        string filePath = filePathToDecrypt.Substring(0, filePathToDecrypt.Length - 4);
                        string directory = Path.GetDirectoryName(filePath);
                        string fileNameOnly = Path.GetFileNameWithoutExtension(filePath);
                        string extension = Path.GetExtension(filePath);

                        // 4. Składamy nową nazwę: katalog + nazwa + przyrostek + rozszerzenie
                        // Wynik: "C:\foto\wakacje_kopia.png"
                        string newFileName = fileNameOnly + "_odszyfrowane" + extension;
                        string outputPath = Path.Combine(directory, newFileName);
                        ProcessFile(filePathToDecrypt, outputPath, StringToByteArray(textBox4.Text), false);
                        MessageBox.Show("Odszyfrowano do:" + outputPath);
                    }
                }
                else
                {
                    MessageBox.Show("Wygeneruj lub podaj 8-znakowy klucz szyfrowania");
                }
            }
            else
            {
                MessageBox.Show("Wybierz plik do zaszyfrowania");
            }
        }

        private void TextEncriptButton_Click(object sender, EventArgs e)
        {
            if (!String.IsNullOrEmpty(textBox1.Text))
            {
                if (!String.IsNullOrEmpty(textBox3.Text))
                {
                    textBox2.Text = Convert.ToBase64String(des.Encrypt(StringToByteArray(textBox1.Text), StringToByteArray(textBox3.Text)));
                }
                else
                {
                    MessageBox.Show("Wygeneruj lub podaj 8-znakowy klucz szyfrowania");
                }
            }
            else
            {
                MessageBox.Show("Wpisz teskt do zaszyfrowania");
            }
        }

        private void TextDecriptButton_Click(object sender, EventArgs e)
        {
            if (!String.IsNullOrEmpty(textBox2.Text))
            {
                if (!String.IsNullOrEmpty(textBox3.Text))
                {
                    textBox1.Text = Encoding.UTF8.GetString(des.Decrypt(Convert.FromBase64String(textBox2.Text), StringToByteArray(textBox3.Text)));
                }
                else
                {
                    MessageBox.Show("Wygeneruj lub podaj 8-znakowy klucz szyfrowania");
                }
            }
            else
            {
                MessageBox.Show("Wpisz teskt do zdeszyfrowania");
            }

        }
        public string GenerateRandomKey()
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            Random random = new Random();

            char[] key = new char[8];

            for (int i = 0; i < 8; i++)
                key[i] = chars[random.Next(chars.Length)];

            return new string(key);
        }

        // Konwertuje tekst (string) na tablicę bajtów
        public byte[] StringToByteArray(string text)
        {
            return Encoding.UTF8.GetBytes(text);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            textBox4.Text = GenerateRandomKey();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            textBox3.Text = GenerateRandomKey();
        }

        public void ProcessFile(string inputPath, string outputPath, byte[] key, bool encrypt)
        {
            byte[] fileBytes = File.ReadAllBytes(inputPath);
            byte[] processedBytes;

            if (encrypt)
            {
                processedBytes = des.Encrypt(fileBytes, key);
            }
            else
            {
                processedBytes = des.Decrypt(fileBytes, key);
            }

            File.WriteAllBytes(outputPath, processedBytes);
        }
    }
}
