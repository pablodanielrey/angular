from Mailman import mm_cfg
import sys

def mod(list):
    for member in list.getMembers():
        if list.getMemberOption(member, mm_cfg.Moderate):
            print member, "is moderated"

def set(list, member, value):
    value = not not (int(value))
    if list.isMember(member):
        list.Lock()
        list.setMemberOption(member, mm_cfg.Moderate, value)
        print "%s's moderated flag set to %d" % (member, value)
        list.Save()
        list.Unlock()
    else:
        print member, "not a member"
