import subprocess as sub

def cmd_formatter(cmd_output) -> list[str]:
        '''Formats CMD output to more readable form.'''
        cmd_output = str(cmd_output)[2:-1]
        output = ""
        for index, char in enumerate(cmd_output):
            try:
                  r_flag_check = (cmd_output[index]+cmd_output[index+1])
                  if r_flag_check != "r\\":
                        output+=char
                        
            except IndexError:
                  pass
        
        return output[:-2].replace("\\xff", " ").strip(" ").split("\\\\n")
       
    
# test space

# out = sub.run(["ipconfig", "/all"], capture_output=True)
# print(cmd_formatter(out.stdout))
# for row in cmd_formatter(out.stdout):
#     if row.find("Physical Address") != -1:
#         print(row[row.find(":")+1:])

# key_list = []
# out = sub.run(["systeminfo"], capture_output=True)
# for row in cmd_formatter(out.stdout):
#       # print(row)
#       if row.lower().find("virtual") != -1:
#             key_list.append(row[row.find(":")+1:])

# print(key_list)

# command, searched_key = "ipconfig /all", "Physical Address"
# key_list = []
# command = command.split()
# out = sub.run(command, capture_output=True)
# for row in cmd_formatter(out.stdout):
#       print(row)
#       if row.lower().find(searched_key) != -1:
#             key_list.append(row[row.find(":")+1:])
# print(key_list)