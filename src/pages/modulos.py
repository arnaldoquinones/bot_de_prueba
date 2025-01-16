class MessageFormStateV2(rx.State):
    show_popover: bool = False

    def toggle_popover(self):
        """Toggle popover visibility."""
        self.show_popover = not self.show_popover