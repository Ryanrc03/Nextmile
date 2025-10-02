import unittest
from rag_system_project.rag_core.rag_simple import ResumeRAGCore

class TestResumeRAGCore(unittest.TestCase):

    def setUp(self):
        self.rag_core = ResumeRAGCore()

    def test_load_data(self):
        # Test loading sample data
        data = self.rag_core.data
        self.assertGreater(len(data), 0, "Data should be loaded successfully.")

    def test_preprocess_data(self):
        # Test preprocessing of data
        self.rag_core._preprocess_data()
        self.assertTrue(hasattr(self.rag_core, 'processed_data'), "Processed data should be available.")
        self.assertGreater(len(self.rag_core.processed_data), 0, "Processed data should not be empty.")

    def test_retrieve(self):
        # Test retrieval of documents
        query = "AI/ML Engineer"
        results = self.rag_core.retrieve(query)
        self.assertGreater(len(results), 0, "Should retrieve relevant documents for the query.")

    def test_generate_prompt(self):
        # Test prompt generation
        query = "Tell me about my experience as an AI/ML Engineer."
        retrieved_docs = self.rag_core.retrieve("AI/ML Engineer")
        prompt = self.rag_core.generate_prompt(query, retrieved_docs)
        self.assertIn("User Question:", prompt, "Prompt should contain the user question.")

    def test_generate_response(self):
        # Test response generation
        query = "What have I done as an AI/ML Engineer?"
        retrieved_docs = self.rag_core.retrieve("AI/ML Engineer")
        prompt = self.rag_core.generate_prompt(query, retrieved_docs)
        response = self.rag_core.generate_response(prompt)
        self.assertIsInstance(response, str, "Response should be a string.")

if __name__ == '__main__':
    unittest.main()