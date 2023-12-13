from in_memory_file_system import InMemoryFileSystem


def execute_command(file_system,command):
    command_parts = command.split()
    if (len(command_parts)==0):
        return
    elif command_parts[0] == 'mkdir':
        if(len(command_parts)==2):
            file_system.mkdir(command_parts[1])
        else:
            file_system.error('mkdir', 'Need folder name to create folder')
    elif command_parts[0] == 'cd':
        file_system.cd(command_parts[1] if len(command_parts) > 1 else None)
    
    elif command_parts[0] == 'ls':
        file_system.ls(command_parts[1] if len(command_parts) > 1 else None)
    
    elif command_parts[0] == 'touch':
        if(len(command_parts)==2):
            file_system.touch(command_parts[1])
        else:
            file_system.error('touch', 'Need Arguments to create file')
    
    elif command_parts[0] == 'echo':
        if(len(command_parts)==4):
            file_name = command_parts[-1]
            text = ' '.join(command_parts[1:-2])  
            file_system.echo(text, file_name)
        else:
            file_system.error('echo', 'Need Arguments to create file')

    elif command_parts[0] == 'mv':
        if(len(command_parts)==3):
            file_system.mv(command_parts[1], command_parts[2])
        else:
            file_system.error('mv', 'Need source and destination argument')
    
    elif command_parts[0] == 'cp':
        if(len(command_parts)==3):
            file_system.cp(command_parts[1], command_parts[2])
        else:
            file_system.error('cp', 'Need source and destination argument')
    
    elif command_parts[0] == 'rm':
        if(len(command_parts)==2):
            file_system.rm(command_parts[1])
        else:
            file_system.error('rm', 'Need file/folder to delete ')
    
    elif command_parts[0] == 'grep':
        if(len(command_parts)==3):
            file_system.grep(command_parts[1], command_parts[2])
        else:
            file_system.error('grep', 'Need filename and string to search ')
    
    elif command_parts[0] == 'pwd':
            file_system.pwd()
    
    elif command_parts[0] == 'cat':
        if(len(command_parts)==2):
            file_system.cat(command_parts[1])
        else:
            file_system.error('cat', 'Need  filename to display ')
    elif command_parts[0] == 'save_state':
        if(len(command_parts)==2):
            file_system.save_state(command_parts[1])
        else:
            file_system.error('save_state', 'Need  filename to save_state ')
    elif command_parts[0] == 'load_state':
        if(len(command_parts)==2):
            file_system.load_state(command_parts[1])
        else:
            file_system.error('load_state', 'Need  filename to save_state ')

def main():
    file_system = InMemoryFileSystem()
    while True:
        command=input("ubuntu-(💀)-InMemoryFileSystem $ ")
        #command = input("Enter a command (type 'exit' to quit): > ")
        if command == 'exit':
            break
        execute_command(file_system,command)

if __name__ == "__main__":
    main()