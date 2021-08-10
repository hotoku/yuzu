import hashlib
import os
import pickle
from functools import wraps
import shutil

from . import logging

USE_CACHE = True
LOGGER = logging.get_logger(__file__)
CACHE_DIR = ".cache"

os.makedirs(CACHE_DIR, exist_ok=True)


def activate_cache(flag):
    global USE_CACHE
    USE_CACHE = flag


def clear_cache():
    shutil.rmtree(CACHE_DIR)
    os.makedirs(CACHE_DIR)


def cache(ignore_args=[], ignore_kw=[]):
    def annotator(f):
        @wraps(f)
        def executor(*args, **kw):
            args_ = [a for i, a in enumerate(args) if i not in ignore_args]
            kw_ = {k: v for k, v in kw.items() if k not in ignore_kw}
            keys = sorted(kw_)
            kw2 = {k: kw_[k] for k in keys}
            key = {"args": args_, "kw": kw2}
            bytes = pickle.dumps(key)
            hash = hashlib.sha256(bytes).hexdigest()
            fpath = f".cache/{f.__module__}.{f.__qualname__}-{hash}"
            cache_exist = os.path.exists(fpath)
            LOGGER.info("%s: cache_exist=%s USE_CACHE=%s",
                        f.__name__, cache_exist, USE_CACHE)
            if not cache_exist or not USE_CACHE:
                LOGGER.info("%s: calculating", f.__name__)
                ret = f(*args, **kw)
                with open(fpath, "wb") as fp:
                    pickle.dump(ret, fp)
                return ret
            else:
                LOGGER.info("%s: reading cache", f.__name__)

                with open(fpath, "rb") as fp:
                    return pickle.load(fp)

        return executor

    return annotator
