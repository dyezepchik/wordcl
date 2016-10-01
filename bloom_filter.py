# -*- encoding: utf-8 -*-
"""
Requires the bitarray library: http://pypi.python.org/pypi/bitarray/

    >>> from bloom_filter import BloomFilter
    >>> f = BloomFilter(capacity=10000, error_rate=0.001)
    >>> for i in range(f.capacity):
    ...     _ = f.put(i)
    ...
    >>> 0 in f
    True
    >>> f.capacity in f
    False
    >>> len(f) <= f.capacity
    True
    >>> (1.0 - (len(f) / float(f.capacity))) <= f.error_rate + 2e-18
    True
"""

import math
import hashlib
from struct import unpack, pack

try:
    import bitarray
except ImportError:
    raise ImportError('pybloom requires bitarray >= 0.3.4')


def make_hashfuncs(num_slices, num_bits):
    if num_bits >= (1 << 31):
        fmt_code, chunk_size = 'Q', 8
    elif num_bits >= (1 << 15):
        fmt_code, chunk_size = 'I', 4
    else:
        fmt_code, chunk_size = 'H', 2
    total_hash_bits = 8 * num_slices * chunk_size
    if total_hash_bits > 384:
        hashfn = hashlib.sha512
    elif total_hash_bits > 256:
        hashfn = hashlib.sha384
    elif total_hash_bits > 160:
        hashfn = hashlib.sha256
    elif total_hash_bits > 128:
        hashfn = hashlib.sha1
    else:
        hashfn = hashlib.md5
    fmt = fmt_code * (hashfn().digest_size // chunk_size)
    num_salts, extra = divmod(num_slices, len(fmt))
    if extra:
        num_salts += 1
    salts = tuple(hashfn(hashfn(pack('I', i)).digest()) for i in range(num_salts))

    def _make_hashfuncs(key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        else:
            key = str(key).encode('utf-8')
        i = 0
        for salt in salts:
            h = salt.copy()
            h.update(key)
            for uint in unpack(fmt, h.digest()):
                yield uint % num_bits
                i += 1
                if i >= num_slices:
                    return

    return _make_hashfuncs


class BloomFilter(object):

    def __init__(self, capacity, error_rate=0.001):
        """Implements a space-efficient probabilistic data structure

        capacity
            this BloomFilter must be able to store at least *capacity* elements
            while maintaining no more than *error_rate* chance of false
            positives
        error_rate
            the error_rate of the filter returning false positives. This
            determines the filters capacity. Inserting more than capacity
            elements greatly increases the chance of false positives.

        >>> b = BloomFilter(capacity=100000, error_rate=0.001)
        >>> b.put("test")
        False
        >>> "test" in b
        True

        """
        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")
        if not capacity > 0:
            raise ValueError("Capacity must be > 0")
        # given M = num_bits, k = num_slices, P = error_rate, n = capacity
        #       k = log2(1/P)
        # solving for m = bits_per_slice
        # n ~= M * ((ln(2) ** 2) / abs(ln(P)))
        # n ~= (k * m) * ((ln(2) ** 2) / abs(ln(P)))
        # m ~= n * abs(ln(P)) / (k * (ln(2) ** 2))
        num_slices = int(math.ceil(math.log(1.0 / error_rate, 2)))
        bits_per_slice = int(math.ceil((capacity * abs(math.log(error_rate))) /
                                       (num_slices * (math.log(2) ** 2))))

        self.error_rate = error_rate
        self.num_slices = num_slices
        self.bits_per_slice = bits_per_slice
        self.capacity = capacity
        self.num_bits = num_slices * bits_per_slice
        self.count = 0
        self.make_hashes = make_hashfuncs(self.num_slices, self.bits_per_slice)

        self.bitarr = bitarray.bitarray(self.num_bits, endian='little')
        self.bitarr.setall(False)

    def __contains__(self, key):
        """Tests a key's membership in this bloom filter.

        >>> b = BloomFilter(capacity=100)
        >>> b.put("hello")
        False
        >>> "hello" in b
        True

        """
        bits_per_slice = self.bits_per_slice
        bit_array = self.bitarr
        hashes = self.make_hashes(key)
        offset = 0
        for k in hashes:
            if not bit_array[offset + k]:
                return False
            offset += bits_per_slice
        return True

    def __len__(self):
        """Return the number of keys stored by this bloom filter."""
        return self.count

    def put(self, key, skip_check=False):
        """ Adds a key to this bloom filter. If the key already exists in this
        filter it will return True. Otherwise False.

        >>> b = BloomFilter(capacity=100)
        >>> b.put("hello")
        False
        >>> b.put("hello")
        True
        >>> b.count
        1

        """
        bit_array = self.bitarr
        bits_per_slice = self.bits_per_slice
        hashes = self.make_hashes(key)
        found_all_bits = True
        if self.count > self.capacity:
            raise IndexError("BloomFilter is at capacity")
        offset = 0
        for k in hashes:
            if not skip_check and found_all_bits and not bit_array[offset + k]:
                found_all_bits = False
            self.bitarr[offset + k] = True
            offset += bits_per_slice

        if skip_check:
            self.count += 1
            return False
        elif not found_all_bits:
            self.count += 1
            return False
        else:
            return True


if __name__ == "__main__":
    b = BloomFilter(capacity=600000, error_rate=0.001)
    b.put("test")
    print("test" in b)