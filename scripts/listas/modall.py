from Mailman import mm_cfg
import sys

def mod(list):
    for member in list.getMembers():
        if list.getMemberOption(member, mm_cfg.Moderate):
            print member, "is moderated"

def set(list, value):
    value = not not (int(value))
    list.Lock()
    try:
        for member in list.getMembers():
            list.setMemberOption(member, mm_cfg.Moderate, value)
            print "."
            #print "%s's moderated flag set to %d" % (member, value)
        list.Save()
    finally:
        list.Unlock()
