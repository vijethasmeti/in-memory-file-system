import os
import json

from Node import Node

class InMemoryFileSystem:
    def __init__(self):
        self.root = Node('/', is_dir=True)
        self.current_node = self.root

    def mkdir(self, directory_name):
        new_directory = Node(directory_name, is_dir=True, parent=self.current_node)
        self.current_node.children[directory_name] = new_directory

    def touch(self, file_name):
        new_file = Node(file_name, parent=self.current_node)
        self.current_node.children[file_name] = new_file

    def pwd(self):
        print(self.get_current_path())    

    
    def cd(self, target_path):
        if target_path == '/' or target_path==None:
            self.current_node = self.root
        elif target_path == '..':
            if self.current_node != self.root:
                self.current_node = self.current_node.parent
        else:
            node = self.get_node_by_path(target_path)
            if node:
                if node.is_dir==False : 
                   print(f"Error: '{target_path}' is a file") 
                self.current_node = node
            else:
                print(f"Error: Invalid path '{target_path}'")

    def ls(self, target_path=None):
        if target_path is None:
            target_path = self.get_current_path()

        node = self.get_node_by_path(target_path)
        if node:
            contents = [child.name for child in node.children.values()]
            print('   '.join(contents))
        else:
            print(f"Error: Invalid path '{target_path}'")

    def echo(self, text, file_name):
        file_node = self.current_node.children.get(file_name)
        if file_node:
            file_node.content = text
        else:
            print(f"Error: File '{file_name}' does not exist")

    def mv(self, source_path, destination_path):
        source_node = self.get_node_by_path(source_path)
        if source_node:
            destination_parent_path, destination_name = os.path.split(destination_path)
            destination_parent_node = self.get_node_by_path(destination_parent_path)

            if destination_parent_node and destination_name:
                # Copy the source node to the new destination
                new_node = self.copy_node(source_node, destination_name)

                # Add the copied node to the destination parent
                destination_parent_node.children[destination_name] = new_node

                # Remove the source node from its current location
                del self.current_node.children[source_node.name]

                print(f"Moved '{source_path}' to '{destination_path}'")
            else:
                print(f"Error: Invalid destination path '{destination_path}'")
        else:
            print(f"Error: Source path '{source_path}' not found")


    def copy_node(self, node, destination_name):
        new_node = Node(name=destination_name, is_dir=node.is_dir, content="" if node.is_dir else node.content, parent=None)

        # Recursively copy children and update parent references
        for child_name, child_node in node.children.items():
            new_child_node = self.copy_node(child_node, child_node.name)
            new_child_node.parent = new_node
            new_node.children[child_name] = new_child_node

        return new_node


    def cp(self, source_path, destination_path):
        source_node = self.get_node_by_path(source_path)
        if source_node:
            destination_parent_path, destination_name = os.path.split(destination_path)
            destination_parent_node = self.get_node_by_path(destination_parent_path)

            if destination_parent_node and destination_name:
                destination_parent_node.children[destination_name] = self.copy_node(source_node,destination_name)
                #print(f"Copied '{source_path}' to '{destination_path}'")
            else:
                print(f"Error: Invalid destination path '{destination_path}'")
        else:
            print(f"Error: Source path '{source_path}' not found")

    def rm(self, target_path):
        target_node = self.get_node_by_path(target_path)
        if target_node:
            del self.current_node.children[os.path.basename(target_path)]
            #print(f"Removed '{target_path}'")
        else:
            print(f"Error: Path '{target_path}' not found")

    def grep(self, pattern, file_path):
        file_node = self.get_node_by_path(file_path)
        if file_node and not file_node.is_dir:
            content = file_node.content
            if pattern in content:
                print(f"Pattern '{pattern}' found in '{file_path}'")
            else:
                print(f"Pattern '{pattern}' not found in '{file_path}'")
        else:
            print(f"Error: File '{file_path}' not found")

    def cat(self, file_path):
        file_node = self.get_node_by_path(file_path)
        if file_node and not file_node.is_dir:
            content = file_node.content
            print(content)
        else:
            print(f"Error: File '{file_path}' not found")

    def get_current_path(self):
        path = []
        current = self.current_node
        while current and current!=self.root:
            path.insert(0, current.name)
            current = current.parent
        return '/' + '/'.join(path)

    def get_node_by_path(self, target_path):
        target_path = os.path.normpath(os.path.join(self.get_current_path(), target_path))
        current = self.root
        for part in os.path.normpath(target_path).split(os.path.sep):
            if part:
                current = current.children.get(part)
                if not current:
                    return None
        return current

    def save_state(self, path):
        with open(path, 'w') as file:
            json.dump({'current_path': self.get_current_path(), 'file_system': self.serialize_tree(self.root)}, file)
        print(f"File system state saved to {path}")

    def load_state(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
            self.root = self.deserialize_tree(data['file_system'])
            self.current_node = self.get_node_by_path(data['current_path'])
        print(f"File system state loaded from {path}")

    

    def serialize_tree(self, node):
        print(node.content,node.name)
        serialized = {'name': node.name, 'is_dir': node.is_dir, 'content': node.content, 'children': {}}
        for child_name, child_node in node.children.items():
            serialized['children'][child_name] = self.serialize_tree(child_node)
        return serialized

    def deserialize_tree(self, serialized):
        print(serialized)
        node = Node(serialized['name'], is_dir=serialized['is_dir'], content=serialized['content'])
        for child_name, child_data in serialized['children'].items():
            child_node = self.deserialize_tree(child_data)
            child_node.parent = node  
            node.children[child_name] = child_node
        return node
    
    
    def error(self,command,text):
        print(command ,text)