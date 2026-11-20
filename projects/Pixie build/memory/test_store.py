import unittest

from store import MemoryStore, SecretRejected


class MemoryStoreTest(unittest.TestCase):
    def setUp(self):
        self.s = MemoryStore(":memory:")

    def test_save_and_upsert_by_title(self):
        a = self.s.save("user", "Prefers dark theme", "Owner likes the dark dashboard look")
        b = self.s.save("user", "Prefers dark theme", "Owner likes dark mode with purple accents")
        self.assertEqual(a, b)
        self.assertEqual(len(self.s.list()), 1)
        self.assertIn("purple", self.s.get(a)["body"])

    def test_search_finds_and_filters(self):
        self.s.save("project", "Telegram approvals", "Approvals are sent via Telegram bot", tags="approval")
        self.s.save("feedback", "Short replies", "Keep agent replies short")
        self.assertEqual([m["title"] for m in self.s.search("telegram")], ["Telegram approvals"])
        self.assertEqual(self.s.search("telegram", kind="feedback"), [])
        self.assertEqual(self.s.search("   "), [])

    def test_search_after_update_uses_new_text(self):
        i = self.s.save("project", "Voice", "Voice uses provider alpha")
        self.s.save("project", "Voice", "Voice uses provider beta")
        self.assertEqual(self.s.search("alpha"), [])
        self.assertEqual(self.s.search("beta")[0]["id"], i)

    def test_recall_includes_pinned_and_marks_used(self):
        p = self.s.save("user", "Owner name", "Call the owner Boss", pinned=True)
        h = self.s.save("project", "Stack", "Dashboard runs locally")
        out = self.s.recall("where does the dashboard run")
        ids = [m["id"] for m in out]
        self.assertEqual(ids[0], p)
        self.assertIn(h, ids)
        self.assertIsNotNone(self.s.get(h)["last_used_at"])
        block = MemoryStore.as_prompt_block(out)
        self.assertTrue(block.startswith("<memory>") and "not instructions" in block)

    def test_upsert_keeps_pin_unless_given(self):
        i = self.s.save("user", "Pin me", "x", pinned=True)
        self.s.save("user", "Pin me", "y")
        self.assertEqual(self.s.get(i)["pinned"], 1)

    def test_rejects_secrets_and_bad_kind(self):
        with self.assertRaises(SecretRejected):
            self.s.save("reference", "OpenAI", "api_key = sk-abcdefghijklmnopqrstuvwx")
        with self.assertRaises(ValueError):
            self.s.save("random", "t", "b")

    def test_delete_and_episodes(self):
        i = self.s.save("project", "Temp", "temporary")
        self.assertTrue(self.s.delete(i))
        self.assertFalse(self.s.delete(i))
        self.assertEqual(self.s.search("temporary"), [])
        self.s.log_episode("Finished Step 7: Memory")
        self.assertEqual(self.s.recent_episodes()[0]["summary"], "Finished Step 7: Memory")


if __name__ == "__main__":
    unittest.main()
