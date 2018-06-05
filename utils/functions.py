
import random


def get_ticket():
    s = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    ticket = 'TK_' + ticket
    return ticket