import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QCheckBox, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt

from parser import parse_and_save
from inference import run_inference

class DocGenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Project Documentation Generator")
        self.setMinimumWidth(500)

        # Repo path input
        self.repo_label = QLabel("Repository Path:")
        self.repo_input = QLineEdit()
        self.repo_browse = QPushButton("Browse")
        self.repo_browse.clicked.connect(self.browse_repo)

        # Local model checkbox + input
        self.local_model_checkbox = QCheckBox("Use local model")
        self.local_model_checkbox.stateChanged.connect(self.toggle_local_model_field)
        self.local_model_input = QLineEdit()
        self.local_model_input.setPlaceholderText("Path to local model folder")
        self.local_model_input.setDisabled(True)
        self.model_browse = QPushButton("Browse")
        self.model_browse.clicked.connect(self.browse_model)
        self.model_browse.setDisabled(True)

        # Feature checkboxes
        self.readme_checkbox = QCheckBox("Generate README")
        self.readme_checkbox.setChecked(True)
        self.comments_checkbox = QCheckBox("Generate Comments")
        self.comments_checkbox.setChecked(True)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_tool)

        # Log output area
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(150)

        # Layout setup
        layout = QVBoxLayout()

        repo_layout = QHBoxLayout()
        repo_layout.addWidget(self.repo_input)
        repo_layout.addWidget(self.repo_browse)

        model_layout = QHBoxLayout()
        model_layout.addWidget(self.local_model_input)
        model_layout.addWidget(self.model_browse)

        layout.addWidget(self.repo_label)
        layout.addLayout(repo_layout)
        layout.addWidget(self.readme_checkbox)
        layout.addWidget(self.comments_checkbox)
        layout.addWidget(self.local_model_checkbox)
        layout.addLayout(model_layout)
        layout.addWidget(self.run_button)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def browse_repo(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Repository Folder")
        if folder:
            self.repo_input.setText(folder)

    def browse_model(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Local Model Folder")
        if folder:
            self.local_model_input.setText(folder)

    def toggle_local_model_field(self, state):
        enabled = state == Qt.Checked
        self.local_model_input.setEnabled(enabled)
        self.model_browse.setEnabled(enabled)

    def run_tool(self):
        self.setWindowTitle("Processing...")
        self.log_output.clear()

        repo_path = self.repo_input.text().strip()
        use_local_model = self.local_model_checkbox.isChecked()
        model_path = self.local_model_input.text().strip() if use_local_model else None
        generate_readme = self.readme_checkbox.isChecked()
        generate_comments = self.comments_checkbox.isChecked()

        if not repo_path or not os.path.isdir(repo_path):
            QMessageBox.critical(self, "Error", "Please select a valid repository path.")
            return

        if use_local_model and (not model_path or not os.path.isdir(model_path)):
            QMessageBox.critical(self, "Error", "Please select a valid local model path.")
            return

        try:
            self.log_output.append("📁 Parsing repository...")
            parse_and_save(repo_path)
            self.log_output.append("✅ Repository parsed successfully.")

            self.log_output.append("🚀 Running inference...")
            run_inference(
                repo=repo_path,
                use_local_model=use_local_model,
                local_model_path=model_path,
                generate_readme=generate_readme,
                generate_comments=generate_comments
            )
            self.log_output.append("✅ Inference complete.")

        except Exception as e:
            self.log_output.append(f"❌ Error: {str(e)}")

        QMessageBox.information(self, "Done", "✅ Documentation generation complete.")
        self.setWindowTitle("AI Project Documentation Generator")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DocGenApp()
    window.show()
    sys.exit(app.exec_())
