import os
import pygame
from pygame.locals import *


def load_image(img, colorkey=None, tp=None):  # Loads an image
    fullimg = os.path.join('img', img)
    try:
        image = pygame.image.load(fullimg)
    except pygame.error, message:
        print 'Cannot load image:', fullimg
        raise SystemExit, message
    if tp is not None:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(snd):  # Loads a sound from the sfx folder
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullsound = os.path.join('sfx', snd)
    try:
        sound = pygame.mixer.Sound(fullsound)
    except pygame.error, message:
        print 'Cannot load sound:', fullsound
        raise SystemExit, message
    return sound


def load_music(musicfile):  # Loads a music file from the music folder
    class NoneMusic:
        def playmusic(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneMusic()
    fullmusic = os.path.join('music', musicfile)
    try:
        music = pygame.mixer.music.load(fullmusic)
    except pygame.error, message:
        print 'Cannot load music file:', fullmusic
        raise SystemExit, message
    return music


def load_sliced_sprites(w, h, filename, animated=[]):
    '''
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
        Assuming you ressources directory is named "ressources"
    '''
    images = []
    master_image = pygame.image.load(os.path.join('img', filename))
    master_image.convert_alpha()

    master_width, master_height = master_image.get_size()
    if not animated:
        for o in xrange(int(master_width/w)):
            animated.append(0)
    for j in xrange(int(master_width/w)):
        sprites = []
        if animated[j]:
            for i in xrange(int(master_height/h)):
                sprites.append(master_image.subsurface((j*w, i*h, w, h)))
            images.append(sprites)
        else:
            images.append(master_image.subsurface((j*w, 0, w, h)))

    return images


def load_files(path, extension):
    list_files = os.listdir(path)
    files = []
    for file in list_files:
        if file.endswith(extension):
            files.append(file)
    return files


def get_vorbis_info(filename):
    """
    Parses the given input file and returns the vorbis comments as a dictionary
    """
    comments = {}
    fp = open("music/"+filename)

    # Read in the file
    data = fp.read().split('vorbis')[2]
    fp.close()

    # Read in the length of the first field (vendor string)
    fieldLen = int(''.join([str(ord(c)) for c in data[3::-1]]))

    # Remove the first field (vendor string)
    data = data[fieldLen+4:]

    # Read in the length of the comment fields
    numComments = int(''.join([str(ord(c)) for c in data[3::-1]]))

    # Remove the comment field length data
    data = data[4:]

    # Read in the comment fields
    for i in range(numComments):
        fieldLen = int(''.join([str(ord(c)) for c in data[3::-1]]))
        fieldData = data[4:fieldLen+4].split('=')

        comments[fieldData[0]] = fieldData[1]

        data = data[fieldLen+4:]

    return comments
