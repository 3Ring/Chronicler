
class Convert():
    def model_replace(self, line: str) -> str:
        '''Replace all instances of flag.attribute with its corresponding value '''
        if not line:
            return ""
        if line.find(f"{self.flag}.") == -1:
            return line
        end = line.find(f"{self.flag}.")+len(self.flag)
        final = len(line)
        for i, l in enumerate(line[end:]):
            if l == " ":
                final = i+end
                break
        attr = getattr(self.model, line[end+1:final], None)
        new = "{{ " + f"{self.flag}.{line[end+1:final]}" + " }}"
        line = line.replace(new, str(attr))
        index = line.find(str(attr)) + len(str(attr))
        return line[:index] + self.model_replace(line[index:])

    def variable_check(self) -> str:
        """checks if there is a Jinja variable in the string and passes it on"""

        if "{{" not in self.line:
            return self.line
        line = self.line.replace("{{ " + "current_user.id" + " }}", str(self.target_user))
        line = line.replace("{{ " + "id" + " }}", str(self.game_id))
        line = self.model_replace(line)
        return line