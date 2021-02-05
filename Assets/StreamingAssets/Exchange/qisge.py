import json
from os.path import dirname, abspath, join


def _read(filename):
    '''Returns the contents of the given file.'''
    filename=join( dirname(abspath(__file__)), filename)
    with open(filename,'r') as file:
        return file.read()
      
def _write(filename,message):
    '''Writes the given message to the given file.'''
    filename=join( dirname(abspath(__file__)), filename)
    with open(filename,'w') as file:
        file.write(message)

def _scrub():
    '''Empties the files 'sprite.txt' and 'input.txt'.'''
    _write('sprite.txt','')
    _write('input.txt','')

def _get_input():
    '''Returns the dictionary of inputs from 'input.txt' and empties the file.'''
    raw_input = _read('input.txt')
    _write('input.txt','')
    if raw_input:
        input = json.loads(raw_input)
    else:
        input = {'key_presses': [], 'clicks': []}
    return input

def _update_screen():
    '''Gets the changes from the `_engine` and writes them to 'sprite.txt'.'''
    changes = _engine.get_changes()
    if changes:
        _write('sprite.txt',changes)

def _val_change(key,value,dictionary):
    '''Returns whether the given dictionary has the given value at the given key.'''
    if key in dictionary:
        val_change = dictionary[key]!=value
    else:
        val_change = True
    return val_change

def update():
    '''Update screen and get input.'''
    _update_screen()
    return _get_input()


class _Engine():
    
    def __init__(self):
        self.image_changes = []
        self.sprite_changes = []
        self.camera_changes = {}
        self.text_changes = []
        self.sound_changes = []
        self.channel_changes = []
                
    def get_changes(self):
        # read in any changes that have not yet been acted upon
        changes = _read('sprite.txt')
        if changes:
            changes = json.loads(changes)
        # otherwise construct from changes recorded in this object
        else:
            changes = {}
            for attr in self.__dict__:
                changes[attr] = self.__dict__[attr]
        # empty the record of changes
        self.image_changes = []
        self.camera_changes = {}
        for attr in ['sprite_changes','camera_changes','text_changes','sound_changes','channel_changes']:
            self.__dict__[attr] = [{} for _ in range(len(self.__dict__[attr]))]
        # output the string of changes
        return json.dumps(changes)


class ImageList(list):
    
    def __init__(self,filenames):
        for filename in filenames:
            self.append(filename)
            
    def _record(self,image_id,filename):
        _engine.image_changes.append({'image_id':image_id,'filename':filename})
        
    def __setitem__(self,image_id,filename):
        super().__setitem__(image_id,filename)
        self._record(image_id,filename)
        
    def append(self,filename):
        image_id = len(self)
        super().append(filename)
        self._record(image_id,filename)


class SoundList(list):
    
    def __init__(self,filenames):
        for filename in filenames:
            self.append(filename)
            
    def _record(self,sound_id,filename):
        _engine.sound_changes.append({'sound_id':sound_id,'filename':filename})
        
    def __setitem__(self,sound_id,filename):
        super().__setitem__(sound_id,filename)
        self._record(sound_id,filename)
        
    def append(self,filename):
        sound_id = len(self)
        super().append(filename)
        self._record(sound_id,filename)


class Camera():

    def __init__(self,x=0,y=0,z=0,size=8,angle=0):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle

    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            # record all values whenever something changes (remove once issue is fixed on Unity side)
            for attr in self.__dict__:
                _engine.camera_changes[attr] = self.__dict__[attr]
            # record the updated value for the thing that's changed
            _engine.camera_changes[name] = val
        self.__dict__[name] = val

 
class Sprite():
    def __init__(self,image_id,x=0,y=0,z=0,size=1,angle=0,flip_h=False,flip_v=False):
        
        self.sprite_id = len(_engine.sprite_changes)
        _engine.sprite_changes.append({})
        
        self.image_id = image_id
        self.x = x
        self.y = y
        self.z = z
        self.flip_h = flip_h
        self.flip_v = flip_v
        self.size = size
        self.angle = angle
        
    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            if name!='sprite_id':
                # record all values whenever something changes (remove once issue is fixed on Unity side)
                for attr in self.__dict__:
                    _engine.sprite_changes[self.sprite_id][attr] = self.__dict__[attr]
                # record the updated value for the thing that's changed
                _engine.sprite_changes[self.sprite_id][name] = val
            self.__dict__[name] = val


class Sound():

    def __init__(self,sound_id,playmode=0,volume=1,pitch=0):
        self.channel_id = len(_engine.channel_changes)
        _engine.channel_changes.append({})

        self.sound_id = sound_id
        self.playmode = playmode
        self.volume = 1
        self.pitch = 0

    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            if name!='channel_id':
                # record all values whenever something changes (remove once issue is fixed on Unity side)
                for attr in self.__dict__:
                    _engine.channel_changes[self.channel_id][attr] = self.__dict__[attr]
                # record the updated value for the thing that's changed
                _engine.channel_changes[self.channel_id][name] = val
            self.__dict__[name] = val


class Text():
    def __init__(self,text,width,height,x=0,y=0,z=0,font_size=0,font=0,angle=0):

        self._text_id = len(_engine.text_changes)
        _engine.text_changes.append({})
        
        self.text = text
        self.x = x
        self.y = y
        #self.z = z will be added one day, but not today
        self.font_size = font_size
        self.font = font
        self.width = width
        self.height = height
        self.angle = angle

    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            if name!='text_id':
                # record all values whenever something changes (remove once issue is fixed on Unity side)
                for attr in self.__dict__:
                    _engine.text_changes[self.text_id][attr] = self.__dict__[attr]
                # record the updated value for the thing that's changed
                _engine.text_changes[self.text_id][name] = val
            self.__dict__[name] = val


_scrub()
_engine = _Engine()
camera = Camera()