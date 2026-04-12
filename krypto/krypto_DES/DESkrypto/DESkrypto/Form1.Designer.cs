namespace DESkrypto
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            openFileDialog1 = new OpenFileDialog();
            comboBox1 = new ComboBox();
            panel1 = new Panel();
            button2 = new Button();
            textBox4 = new TextBox();
            label4 = new Label();
            label2 = new Label();
            label1 = new Label();
            DecryptButton = new Button();
            DecryptFileChooseButton = new Button();
            EncryptButton = new Button();
            EncryptFileChooseButton = new Button();
            panel2 = new Panel();
            button1 = new Button();
            label3 = new Label();
            textBox3 = new TextBox();
            TextDecriptButton = new Button();
            TextEncriptButton = new Button();
            textBox2 = new TextBox();
            textBox1 = new TextBox();
            panel1.SuspendLayout();
            panel2.SuspendLayout();
            SuspendLayout();
            // 
            // comboBox1
            // 
            comboBox1.DropDownStyle = ComboBoxStyle.DropDownList;
            comboBox1.FormattingEnabled = true;
            comboBox1.Items.AddRange(new object[] { "Plik", "Tekst" });
            comboBox1.Location = new Point(12, 8);
            comboBox1.Name = "comboBox1";
            comboBox1.Size = new Size(121, 23);
            comboBox1.TabIndex = 0;
            comboBox1.SelectedIndexChanged += comboBox1_SelectedIndexChanged;
            // 
            // panel1
            // 
            panel1.Controls.Add(button2);
            panel1.Controls.Add(textBox4);
            panel1.Controls.Add(label4);
            panel1.Controls.Add(label2);
            panel1.Controls.Add(label1);
            panel1.Controls.Add(DecryptButton);
            panel1.Controls.Add(DecryptFileChooseButton);
            panel1.Controls.Add(EncryptButton);
            panel1.Controls.Add(EncryptFileChooseButton);
            panel1.Location = new Point(12, 37);
            panel1.Name = "panel1";
            panel1.Size = new Size(776, 372);
            panel1.TabIndex = 2;
            panel1.Visible = false;
            // 
            // button2
            // 
            button2.Location = new Point(382, 318);
            button2.Name = "button2";
            button2.Size = new Size(98, 41);
            button2.TabIndex = 7;
            button2.Text = "Wygeneruj losowy klucz";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // textBox4
            // 
            textBox4.Location = new Point(276, 328);
            textBox4.MaxLength = 8;
            textBox4.Name = "textBox4";
            textBox4.Size = new Size(100, 23);
            textBox4.TabIndex = 7;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(46, 331);
            label4.Name = "label4";
            label4.Size = new Size(224, 15);
            label4.TabIndex = 6;
            label4.Text = "Wybierz klucz szyfrowania/deszyfrowania";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(156, 222);
            label2.Name = "label2";
            label2.Size = new Size(38, 15);
            label2.TabIndex = 5;
            label2.Text = "label2";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(156, 64);
            label1.Name = "label1";
            label1.Size = new Size(38, 15);
            label1.TabIndex = 4;
            label1.Text = "label1";
            // 
            // DecryptButton
            // 
            DecryptButton.Location = new Point(46, 260);
            DecryptButton.Name = "DecryptButton";
            DecryptButton.Size = new Size(104, 49);
            DecryptButton.TabIndex = 3;
            DecryptButton.Text = "Zdeszyfruj plik";
            DecryptButton.UseVisualStyleBackColor = true;
            DecryptButton.Click += DecryptButton_Click;
            // 
            // DecryptFileChooseButton
            // 
            DecryptFileChooseButton.Location = new Point(46, 205);
            DecryptFileChooseButton.Name = "DecryptFileChooseButton";
            DecryptFileChooseButton.Size = new Size(104, 49);
            DecryptFileChooseButton.TabIndex = 2;
            DecryptFileChooseButton.Text = "Wybierz plik do zdeszyfrowania";
            DecryptFileChooseButton.UseVisualStyleBackColor = true;
            DecryptFileChooseButton.Click += DecryptFileChooseButton_Click;
            // 
            // EncryptButton
            // 
            EncryptButton.Location = new Point(46, 102);
            EncryptButton.Name = "EncryptButton";
            EncryptButton.Size = new Size(104, 49);
            EncryptButton.TabIndex = 1;
            EncryptButton.Text = "Zaszyfruj plik";
            EncryptButton.UseVisualStyleBackColor = true;
            EncryptButton.Click += EncryptButton_Click;
            // 
            // EncryptFileChooseButton
            // 
            EncryptFileChooseButton.Location = new Point(46, 47);
            EncryptFileChooseButton.Name = "EncryptFileChooseButton";
            EncryptFileChooseButton.Size = new Size(104, 49);
            EncryptFileChooseButton.TabIndex = 0;
            EncryptFileChooseButton.Text = "Wybierz plik do zaszyfrowania";
            EncryptFileChooseButton.UseVisualStyleBackColor = true;
            EncryptFileChooseButton.Click += EncryptFileChooseButton_Click;
            // 
            // panel2
            // 
            panel2.Controls.Add(button1);
            panel2.Controls.Add(label3);
            panel2.Controls.Add(textBox3);
            panel2.Controls.Add(TextDecriptButton);
            panel2.Controls.Add(TextEncriptButton);
            panel2.Controls.Add(textBox2);
            panel2.Controls.Add(textBox1);
            panel2.Location = new Point(12, 37);
            panel2.Name = "panel2";
            panel2.Size = new Size(776, 372);
            panel2.TabIndex = 6;
            // 
            // button1
            // 
            button1.Location = new Point(542, 54);
            button1.Name = "button1";
            button1.Size = new Size(100, 42);
            button1.TabIndex = 6;
            button1.Text = "Wygenereuj losowy klucz";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(542, 7);
            label3.Name = "label3";
            label3.Size = new Size(227, 15);
            label3.TabIndex = 5;
            label3.Text = "Wybierz klucz szyfrowania/deszyfrowania:";
            // 
            // textBox3
            // 
            textBox3.Location = new Point(542, 25);
            textBox3.MaxLength = 8;
            textBox3.Name = "textBox3";
            textBox3.Size = new Size(100, 23);
            textBox3.TabIndex = 4;
            // 
            // TextDecriptButton
            // 
            TextDecriptButton.Location = new Point(366, 300);
            TextDecriptButton.Name = "TextDecriptButton";
            TextDecriptButton.Size = new Size(75, 38);
            TextDecriptButton.TabIndex = 3;
            TextDecriptButton.Text = "Zdeszyfruj tekst";
            TextDecriptButton.UseVisualStyleBackColor = true;
            TextDecriptButton.Click += TextDecriptButton_Click;
            // 
            // TextEncriptButton
            // 
            TextEncriptButton.Location = new Point(116, 300);
            TextEncriptButton.Name = "TextEncriptButton";
            TextEncriptButton.Size = new Size(75, 38);
            TextEncriptButton.TabIndex = 2;
            TextEncriptButton.Text = "Zaszyfruj tekst";
            TextEncriptButton.UseVisualStyleBackColor = true;
            TextEncriptButton.Click += TextEncriptButton_Click;
            // 
            // textBox2
            // 
            textBox2.Location = new Point(285, 3);
            textBox2.Multiline = true;
            textBox2.Name = "textBox2";
            textBox2.ScrollBars = ScrollBars.Vertical;
            textBox2.Size = new Size(251, 291);
            textBox2.TabIndex = 1;
            // 
            // textBox1
            // 
            textBox1.Location = new Point(28, 3);
            textBox1.Multiline = true;
            textBox1.Name = "textBox1";
            textBox1.ScrollBars = ScrollBars.Vertical;
            textBox1.Size = new Size(251, 291);
            textBox1.TabIndex = 0;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(panel1);
            Controls.Add(panel2);
            Controls.Add(comboBox1);
            Name = "Form1";
            Text = "Form1";
            panel1.ResumeLayout(false);
            panel1.PerformLayout();
            panel2.ResumeLayout(false);
            panel2.PerformLayout();
            ResumeLayout(false);
        }

        #endregion
        private OpenFileDialog openFileDialog1;
        public ComboBox comboBox1;
        private Panel panel1;
        private Button EncryptFileChooseButton;
        private Button DecryptButton;
        private Button DecryptFileChooseButton;
        private Button EncryptButton;
        private Label label2;
        private Label label1;
        private Panel panel2;
        private Button TextDecriptButton;
        private Button TextEncriptButton;
        private TextBox textBox2;
        private TextBox textBox1;
        private TextBox textBox3;
        private Label label3;
        private TextBox textBox4;
        private Label label4;
        private Button button2;
        private Button button1;
    }
}
