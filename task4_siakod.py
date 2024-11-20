import json

ORDER = 300
class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BPlusTree:
    def __init__(self):
        self.root = BPlusTreeNode(leaf=True)

    def insert(self, key, file_path):
        root = self.root
        if len(root.keys) < ORDER - 1:
            self._insert_into_leaf(root, key, file_path)
        else:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_into_non_full(self.root, key, file_path)

    def _insert_into_leaf(self, node, key, file_path):
        idx = 0
        while idx < len(node.keys) and node.keys[idx] < key:
            idx += 1
        node.keys.insert(idx, key)
        node.children.insert(idx, file_path)

    def _split_child(self, parent, index):
        child = parent.children[index]
        new_child = BPlusTreeNode(leaf=child.leaf)
        mid = len(child.keys) // 2
        split_key = child.keys[mid]

        new_child.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]

        if child.leaf:
            new_child.children = child.children[mid:]
            child.children = child.children[:mid]

        parent.keys.insert(index, split_key)
        parent.children.insert(index + 1, new_child)

    def _insert_into_non_full(self, node, key, file_path):
        if node.leaf:
            self._insert_into_leaf(node, key, file_path)
        else:
            idx = 0
            while idx < len(node.keys) and node.keys[idx] < key:
                idx += 1
            child = node.children[idx]
            if len(child.keys) == ORDER - 1:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    idx += 1
            self._insert_into_non_full(node.children[idx], key, file_path)

    def find(self, key):
        node = self.root
        while not node.leaf:
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            node = node.children[idx]

        for i, k in enumerate(node.keys):
            if k == key:
                file_path = node.children[i]
                with open(file_path, 'r') as f:
                    profile = json.load(f)
                return profile
        return None


def save_profile_to_file(profile):
    file_name = f"profile_{profile['id']}.json"
    with open(file_name, 'w') as f:
        json.dump(profile, f)
    return file_name


def build_tree_from_json(file_name):
    with open(file_name, 'r') as f:
        profiles = json.load(f)

    tree = BPlusTree()
    for profile in profiles:
        file_path = save_profile_to_file(profile)
        tree.insert(profile['id'], file_path)
    return tree


if __name__ == "__main__":
    tree = build_tree_from_json("data.json")

    profile_id = (input("Введите id профиля для поиска: "))
    profile = tree.find(profile_id)

    if profile:
        print("Найденный профиль:", profile)
    else:
        print("Профиль с таким id не найден.")
