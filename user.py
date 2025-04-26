class HeartStyle:
    def __init__(
            self,
            style_ = 'abstract',
            form_ = 'round',
            color_ = 'red',
            props_ = 'fire',
            size_ = 'medium'
        ):
        self.style_ = style_
        self.form_ = form_
        self.color_ = color_
        self.props_ = props_
        self.size_ = size_

    def to_dict(self):
        return {
            'style': self.style_,
            'form': self.form_,
            'color': self.color_,
            'props': self.props_,
            'size': self.size_
        }
class User:
    def __init__(self, username = None, user_id = None, heart_style = HeartStyle()):
        self.username = username
        self.user_id = user_id
        self.heart_style = heart_style
