import sys
sys.path.append('../python')
sys.path.append('.')

from model.oauth.oauth import OAuth1Model
from main import createTestingContext


if __name__ == '__main__':

    h = sys.argv[1]
    d = sys.argv[2]
    u = sys.argv[3]
    p = sys.argv[4]

    ctx = createTestingContext(h,d,u,p)
    ctx.getConn()
    try:
        OAuth1Model.createClient(ctx)
        ctx.con.commit()
    finally:
        ctx.closeConn()
