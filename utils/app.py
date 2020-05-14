class ModelUtils(object):
    def to_dict(self):
        result = super(ModelUtils, self).to_dict()
        result['id'] = self.key.id()  # get the key as a string
        return result
