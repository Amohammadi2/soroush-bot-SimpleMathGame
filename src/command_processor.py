class Processor:

    def dispatch_command(self, command: dict):
        """dispatches the command and returns a handler

        Args:
            command (dict): the message structure from soroush SDK
        """

        if command["type"] == "START":
            return self.get_start_message

        elif command["type"] == "TEXT":
            self.current_user_id = command["from"]

            if (cmd_txt := command["body"]).startswith("cmd"):
                result = self.__dispatch_command(cmd_txt)
                if result["error"]:
                    return {"error": True}
                return result["dispatched_method"]
        return None

    def get_start_message(self):
        # Todo: implement this method
        raise NotImplemented("this method is not implemented yet")

    def __dispatch_command(self, cmd):
        """dispatches command text to appropriate methods

        Args:
            cmd (str): the command

        Returns:
            dict: {
                dispatched_method: function -> the method that the command was dispatched to
                error: bool -> True if there was any error, False otherwise
                error_msg: str -> (optional) the error message
            }
        """
        get_handler_name = lambda c: c[len("cmd")+1::]

        cmd_handler = getattr(self, get_handler_name(cmd), False)
        if not cmd_handler: 
            return {"error_msg": "command not found", "error": True}
        return {"dispatched_method": cmd_handler, "error": True}

    def start_game(self): pass

    def generate_question(self):
        # Todo: implement this method
        raise NotImplemented("this method is not implemented yet")