import unittest
from blocks import *


class Test_Block_Utilities(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. This is a list
2. Of 3
3. Items

```
This is code
```

# This is a heading

### This is another heading
But this isn't

> Finally a bunch of quotes
> Maybe someone famous
> Maybe not
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        expected_result = [
            BlockType.paragraph,
            BlockType.paragraph,
            BlockType.ul,
            BlockType.ol,
            BlockType.code,
            BlockType.heading,
            BlockType.heading,
            BlockType.quote
        ]

        for block in blocks:
            block_types.append(block_to_block_type(block))

        self.assertListEqual(block_types, expected_result)
