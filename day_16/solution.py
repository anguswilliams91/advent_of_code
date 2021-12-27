"""16. Packet decoder."""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
import sys
from typing import NamedTuple, Optional, Sequence, Tuple, Union

_BIG_INTEGER = sys.maxsize


@dataclass
class Packet:
    version: int
    type_id: int
    value: Optional[int]
    sub_packets: Sequence[Packet]

    def __post_init__(self):
        sub_packet_values = (p.value for p in self.sub_packets)
        if self.type_id == 4:
            pass
        elif self.type_id == 0:
            self.value = sum(sub_packet_values)
        elif self.type_id == 1:
            self.value = reduce(lambda a,b: a *b, sub_packet_values)
        elif self.type_id == 2:
            self.value = min(sub_packet_values)
        elif self.type_id == 3:
            self.value = max(sub_packet_values)
        else:
            first, second = tuple(sub_packet_values)
            if self.type_id == 5:
                self.value = int(first > second)
            elif self.type_id == 6:
                self.value = int(first < second)
            elif self.type_id == 7:
                self.value = int(first == second)

    @property
    def sum_of_versions(self):
        total = self.version
        match (s := self.sub_packets):
            case []:
                return total
            case _:
                return total + sum(p.sum_of_versions for p in s)


class PacketsAndBits(NamedTuple):
    packets: Sequence[Packet]
    bits: str


def calculate_sum_of_versions(hex: str) -> int:
    """Calculates the sum of the versions of a hierarchy of packets."""
    return make_packet_from_hex(hex).sum_of_versions


def calculate_packet_value(hex: str) -> int:
    """Calculates the value of a packet given the type id hierarchy."""
    return make_packet_from_hex(hex).value


def make_packet_from_hex(hex: str) -> Packet:
    """Translates a hex string into a packet."""
    bits = bin(int(hex, 16))[2:].zfill(4 * len(hex))
    [packet] = make_packets_from_binary(bits).packets
    return packet


def make_packets_from_binary(
    bits: str, max_packets: int = _BIG_INTEGER
) -> PacketsAndBits:
    """Translates a binary string into a list of packets and some leftover bits."""
    packets = []
    while (len(packets) < max_packets) and bits:
        version = int(bits[:3], 2)
        type_id = int(bits[3:6], 2)
        bits = bits[6:]
        if type_id == 4:
            value, bits = calculate_literal_value(bits)
            packets.append(
                Packet(
                    version=version,
                    type_id=type_id,
                    value=value,
                    sub_packets=[],
                )
            )
        else:
            length_type_id, bits = bits[0], bits[1:]
            if length_type_id == "0":
                sub_packets, bits = make_subpackets_for_length_id_0(bits)
                packets.append(
                    Packet(
                        version=version,
                        type_id=type_id,
                        value=None,
                        sub_packets=sub_packets,
                    )
                )
            else:
                sub_packets, bits = make_subpackets_for_length_id_1(bits)
                packets.append(
                    Packet(
                        version=version,
                        type_id=type_id,
                        value=None,
                        sub_packets=sub_packets,
                    )
                )
    return PacketsAndBits(packets=packets, bits=bits)


def make_subpackets_for_length_id_0(bits: str) -> Union[Packet, Sequence[Packet]]:
    """Produces a list of packets given the number of bits in those sub packets."""
    num_bits_in_sub_packets = int(bits[:15], 2)
    subpacket_bits = bits[15 : 15 + num_bits_in_sub_packets]
    bits = bits[15 + num_bits_in_sub_packets :]
    if set(bits) == {"0"}:
        bits = ""
    sub_packets = make_packets_from_binary(subpacket_bits).packets
    return PacketsAndBits(packets=sub_packets, bits=bits)


def make_subpackets_for_length_id_1(bits: str) -> Union[Packet, Sequence[Packet]]:
    """Produces a list of subpackets given the total number of sub packets."""
    total_sub_packets = int(bits[:11], 2)
    return make_packets_from_binary(bits[11:], max_packets=total_sub_packets)


def calculate_literal_value(bits: str) -> Tuple[int, str]:
    """Computes the value of a literal type packet."""
    value_bits = ""
    stop = False
    current_bit = 0
    while not stop:
        value_bits += bits[current_bit + 1 : current_bit + 5]
        if bits[current_bit] == "0":
            stop = True
        current_bit = current_bit + 5
    if set(bits[current_bit:]) == {"0"}:
        bits = ""
    return int(value_bits, 2), bits[current_bit:]



if __name__ == "__main__":
    with open("input.txt", "r") as f:
        bits = f.read()

    print(f"Part one: {calculate_sum_of_versions(bits)}")
    print(f"Part two: {calculate_packet_value(bits)}")