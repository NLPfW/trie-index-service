
class TrieIndex(object):
    def __init__(self):
        self.root = {}
        pass

    def add(self, key, encoding='utf-8'):
        ukey = key.decode(encoding)
        p = self.root
        for i, u_char in enumerate(ukey):
            if u_char not in p:
                p[u_char] = {}

            p = p[u_char]

        p["__val"] = 1

    def get(self, key, encoding='utf-8'):
        ukey = key.decode(encoding)
        p = self.root
        for i, u_char in enumerate(ukey):
            if u_char not in p:
                return False
            p = p[u_char]

        return "__val" in p and p["__val"] == 1

    """
    matcher: find the common prefix of a given string and the trie

    @string the given string in bytes
    @begin the start index, ignore the unicode chars before it

    @return generator each time gives the index which it meets
    """
    def matcher(self, string, begin=0):
        string = string.decode('utf-8')[begin:]
        p = self.root
        for i, u_char in enumerate(string):
            p = p[u_char]
            if "__val" in p and p["__val"] == 1:
                yield i + 1

if __name__ == "__main__":
    t = TrieIndex()
    t.add("abcd")
    t.add("abc")

    print "'abcd' and 'abc' added into trie index"

    print "abc in trie:", t.get("abc")
    print "abcd in trie:", t.get("abcd")
    print "ab not in trie:", t.get("ab")
    print "a not in trie:", t.get("a")

    for i in t.matcher("abcd"):
        print "find prefix 0-%d:" % i, ("abcd")[0:i]
