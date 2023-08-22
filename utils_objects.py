class Pagination:
    def __init__(self, number_of_pages=None, current_page=None):
        if current_page == None:
            self.current_page = 1
            self.number_of_pages = 1
        else:
            self.current_page = current_page
        self.number_of_pages = number_of_pages
    
    def has_right_input(self, *inputs):
        status = True
        for test_input in inputs:
            if not test_input:
                status = False
                if not test_input.isinstance(int):
                    status = False
            if not status:
                break
                
        return status

    def has_next(self):
        if self.has_right_input(self.current_page, self.number_of_pages):
            if self.current_page + 1 <= self.number_of_pages:
                return True
            return False

    def has_previous(self):
        if self.has_right_input(self.current_page, self.number_of_pages):
            if self.current_page - 1 >= 1:
                return True
            return False
        
    def set_next_page(self):
        if self.has_next:
            self.current_page += 1
            return self.current_page
        else:
            return None
    
    def set_previous_page(self):
        if self.has_previous:
            self.current_page -= 1
            return self.current_page
        else:
            return None
    