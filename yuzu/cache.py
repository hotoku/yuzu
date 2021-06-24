import pickle
import hashlib
import os
from functools import wraps

from . import logging

USE_CACHE = True
LOGGER = logging.get_logger(__file__)


def activate_cache(flag):
    global USE_CACHE
    USE_CACHE = flag


def cache(ignore_args=[], ignore_kw=[]):
    def annotator(f):
        @wraps(f)
        def executor(*args, NO_USE_CACHE=False, **kw):
            args_ = [
                a for i, a in enumerate(args)
                if i not in ignore_args
            ]
            kw_ = {
                k: v for k, v in kw.items()
                if k not in ignore_kw
            }
            key = {
                "args": args_,
                "kw": kw_
            }
            bytes = pickle.dumps(key)
            hash = hashlib.sha256(bytes).hexdigest()
            fpath = f".cache/{f.__name__}-{hash}"
            cache_exist = os.path.exists(fpath)
            LOGGER.info("%s: cache_exist=%s USE_CACHE=%s NO_USE_CACHE=%s",
                        f.__name__, cache_exist, USE_CACHE, NO_USE_CACHE)
            if not cache_exist or not USE_CACHE or NO_USE_CACHE:
                LOGGER.info("%s: calculating",
                            f.__name__)
                ret = f(*args, **kw)
                with open(fpath, "wb") as fp:
                    pickle.dump(ret, fp)
                return ret
            else:
                LOGGER.info("%s: reading cache",
                            f.__name__)

                with open(fpath, "rb") as fp:
                    return pickle.load(fp)
        return executor
    return annotator
