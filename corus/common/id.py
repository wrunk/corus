#!/usr/bin/env python

# Written by Warren Runk
# This file is free software in the public domain.


import base64
import random
import uuid


"""
Sharded globally unique identifier mini library for python2.7

Version 1.0

Benefits:
    - Uses a standard UUID1 for global uniqueness (see python docs on UUID for exceptions)
    - Semi Ordered Ids (since the first section is from the clock)
    - Fairly small 26 chars using base32
    - 100% url safe (using padding stripped base32 lowered)
    - Sharded/bucketed (first 12 bits of the node param are altered to be a shard ID 0-4095)
    - By adding the shard ID in the node section, we obfuscate the MAC address of the generating computer

Public functions:
    - get_new_guid
    - get_shard_id
    - is_valid_guid

Example GUID: wq5xhtdkyai6jgpn7724fsahjq

Some stats from creating a million GUIDs:

Total # of shard IDs 4096
Max # of GUIDs (298) were created in shard (65)
Min # of GUIDs (190) were created in shard (1405)
Median pos 2047 244
Median pos 2048 244
Median pos 2049 244
Average (Should be 244 - 1mil/4096) 244
Variance 251
Standard Deviation 15.8429795178

Run this script to run tests
"""

# --------------------------------------------------------------------------- #
# Core lib code

__all__ = ['get_new_guid', 'get_shard_id', 'is_valid_guid']
# Cache our hardware MAC address with the shard mask applied
_masked_node = uuid.getnode() & 0x000fffffffff


def is_valid_guid(guid):
    if not isinstance(guid, basestring) or len(guid) != 26:
        return False
    try:
        shard_id = get_shard_id(guid)
    except TypeError:
        return False
    else:
        if not _is_valid_shard_id(shard_id):
            return False
    return True


def _is_valid_shard_id(shard_int_id):
    if not isinstance(shard_int_id, int):
        return False
    if shard_int_id < 0 or shard_int_id > 4095:
        return False
    return True


def get_shard_id(guid):
    """
    Get the numeric shard ID associated with this GUID (0-4095)
    """
    orig_uuid_bytes = base64.b32decode(guid + '======', casefold=True)
    hex_rep = "".join("{:02x}".format(ord(c)) for c in orig_uuid_bytes)
    return int(hex_rep[-12:-9], 16)


def _create_guid(shard_int):
    # Create a binary mask for our shard ID to apply to the node value
    # Will look like 03f000000000
    shard_hex_mask = "%03x" % shard_int + '0' * 9

    # Calculate the final node integer value using binary OR to be passed to the uuid1 creation function
    final_int_val = _masked_node | int(shard_hex_mask, 16)

    # Create the UUID. Hex representations of UUIDs look like b43b73cc-6ac0-11e4-99ed-fff5c2c8074c
    # You can see the fff in the last section is our shard ID
    new_uid = uuid.uuid1(node=final_int_val)

    # Finally, return the finished guid. Will look like wq5xhtdkyai6jgpn7724fsahjq
    return base64.b32encode(new_uid.bytes).lower().rstrip('=')


def get_new_guid(affinity_guid=None, shard_id=None):
    """
    Return a base32 encoded byte string of length 26.

    affinity_guid: pass a previously created GUID. This will create the new GUID in the same shard

    shard_id: pass the shard ID integer between 0 - 4095
    """
    if affinity_guid:
        shard_id = get_shard_id(affinity_guid)
    elif not shard_id:
        shard_id = random.randint(0, 4095)
    if not _is_valid_shard_id(shard_id):
        raise ValueError("Invalid shard ID, not an int or out of range (0-4095)")
    return _create_guid(shard_id)


# --------------------------------------------------------------------------- #
# Tests, stats, and helpers

def _test_print_sample():
    print "***** Creating and printing some sample GUIDs"
    for i in range(20):
        u = get_new_guid()
        print "GUID: (%s) LEN (%i)" % (u, len(u))


def _test_create_many():
    """Note Creating the 1mil guids here will eat about ~200 RAM and take a while so use at own risk"""

    # Normally you would use a set or something, but doing guid in dict is MUCH faster than guid in list/set
    guids = {}
    # Let's track our shard distribution
    shard_heat_map = {}

    for i in range(1000000):
        guid = get_new_guid()
        assert guid not in guids, 'dup'
        guids[guid] = ''

        # Record the bucket
        shard_id = get_shard_id(guid)
        if shard_id not in shard_heat_map:
            shard_heat_map[shard_id] = 0
        shard_heat_map[shard_id] += 1

    return shard_heat_map


def _test_print_stats(shard_heat_map):
    mi = 200000
    mic = None
    ma = 0
    mac = None
    total = 0
    for k, v in shard_heat_map.items():
        total += v
        if v < mi:
            mic = k
            mi = v
        if v > ma:
            mac = k
            ma = v
    avg = total / len(shard_heat_map)
    vtotal = 0
    for k, v in shard_heat_map.items():
        v = (v - avg) ** 2
        vtotal += v
    vavg = vtotal / len(shard_heat_map)

    print "***** Stats from creating %i GUIDs" % total
    print "Total # of shard IDs", len(shard_heat_map)
    print "Max # of GUIDs (%i) were created in shard (%i)" % (ma, mac)
    print "Min # of GUIDs (%i) were created in shard (%i)" % (mi, mic)
    print "Median pos 2047", sorted(shard_heat_map.values())[2047]
    print "Median pos 2048", sorted(shard_heat_map.values())[2048]
    print "Median pos 2049", sorted(shard_heat_map.values())[2049]
    print "Average (Should be 244 - 1mil/4096)", avg
    print "Variance", vavg

    import math
    print "Standard Deviation", math.sqrt(vavg)


def _test_affinity():
    guid = get_new_guid()
    shard = get_shard_id(guid)
    for i in range(10):
        new_guid = get_new_guid(affinity_guid=guid)
        assert get_shard_id(new_guid) == shard

    for i in range(10):
        new_guid = get_new_guid(shard_id=shard)
        assert get_shard_id(new_guid) == shard

    print "Creating GUIDs with affinity id and shard ID OK"


def _test_is_valid_guid():
    guid = get_new_guid()
    assert is_valid_guid(guid)
    assert not is_valid_guid(guid[1:])
    print "Function is_valid_guid OK"


def run_tests():
    # Test creating a million IDs (make sure they don't dup) and print the stats
    shard_heat_map = _test_create_many()
    _test_print_stats(shard_heat_map)
    _test_affinity()
    _test_is_valid_guid()
    _test_print_sample()


if __name__ == '__main__':
    run_tests()
