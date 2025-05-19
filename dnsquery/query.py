import sys
import dns.resolver
from icecream import ic

def get_all_ips_for_domain(domain):
    """
    주어진 도메인에 연결된 모든 IPv4 및 IPv6 주소를 조회합니다.

    Args:
        domain (str): 조회할 도메인 이름 (예: "google.com").

    Returns:
        tuple:  IPv4 주소 목록과 IPv6 주소 목록을 담은 튜플.
                조회 실패 시 (None, None) 반환.
                레코드가 없으면 빈 리스트를 포함한 튜플 반환.
    """
    ipv4_addresses = []
    ipv6_addresses = []
    found_records = False # 레코드를 하나라도 찾았는지 확인하는 플래그

    print(f"도메인 '{domain}'에 대한 IP 주소 조회를 시작합니다...")

    # IPv4 (A) 레코드 조회
    try:
        # dns.resolver.resolve 함수는 해당 타입의 모든 레코드를 반환합니다.
        answers_a = dns.resolver.resolve(domain, 'A')
        for rdata in answers_a:
            ipv4_addresses.append(rdata.address)
        found_records = True
        print(f"  IPv4 (A) 레코드 {len(ipv4_addresses)}개 발견.")
    except dns.resolver.NoAnswer:
        # 해당 타입의 레코드가 없을 경우 발생하는 예외
        print("  IPv4 (A) 레코드가 없습니다.")
        pass # A 레코드가 없더라도 AAAA 레코드를 시도해야 하므로 예외를 무시하고 진행
    except dns.resolver.NXDOMAIN:
        # 도메인 자체가 존재하지 않을 경우 발생하는 예외
        print(f"오류: 도메인 '{domain}'이 존재하지 않습니다 (NXDOMAIN).", file=sys.stderr)
        return None, None # 도메인 오류를 알리기 위해 None 반환
    except Exception as e:
        # 그 외 DNS 조회 중 발생한 오류
        print(f"IPv4 레코드 조회 중 오류 발생: {e}", file=sys.stderr)
        # 오류 발생 시에도 AAAA 조사를 위해 계속 진행하거나 중단할 수 있습니다. 여기서는 계속 진행.
        pass

    # IPv6 (AAAA) 레코드 조회
    try:
        answers_aaaa = dns.resolver.resolve(domain, 'AAAA')
        for rdata in answers_aaaa:
            ipv6_addresses.append(rdata.address)
        found_records = True
        print(f"  IPv6 (AAAA) 레코드 {len(ipv6_addresses)}개 발견.")
    except dns.resolver.NoAnswer:
        # 해당 타입의 레코드가 없을 경우 발생하는 예외
        print("  IPv6 (AAAA) 레코드가 없습니다.")
        pass # AAAA 레코드가 없더라도 다음 단계로 진행
    except dns.resolver.NXDOMAIN:
        # 도메인 자체가 존재하지 않을 경우 발생하는 예외 (A 레코드에서 이미 잡았을 가능성 높음)
        if not found_records: # A 레코드 조회에서 NXDOMAIN이 아니었을 경우에만 출력
            print(f"오류: 도메인 '{domain}'이 존재하지 않습니다 (NXDOMAIN).", file=sys.stderr)
        return None, None # 도메인 오류를 알리기 위해 None 반환
    except Exception as e:
        # 그 외 DNS 조회 중 발생한 오류
        print(f"IPv6 레코드 조회 중 오류 발생: {e}", file=sys.stderr)
        pass # 오류 발생 시에도 결과 반환을 위해 계속 진행

    # 만약 A, AAAA 모두 조회했으나 어떤 레코드도 찾지 못한 경우 (NoAnswer 예외만 발생한 경우)
    if not found_records and not ipv4_addresses and not ipv6_addresses:
        print(f"알림: 도메인 '{domain}'에 A 또는 AAAA 레코드가 없습니다.", file=sys.stderr)
        # 레코드는 없지만, 도메인 자체는 유효했음을 의미하므로 빈 리스트 반환
        return [], []


    return ipv4_addresses, ipv6_addresses


def find_all_ips_for_domain(domain_to_lookup):
    ipv4_addresses = []

    print(f"도메인 '{domain_to_lookup}'에 대한 IP 주소 조회를 시작합니다...")

    # IPv4 (A) 레코드 조회
    try:
        # dns.resolver.resolve 함수는 해당 타입의 모든 레코드를 반환합니다.
        answers_a = dns.resolver.resolve(domain_to_lookup, 'A')
        for rdata in answers_a:
            ipv4_addresses.append(rdata.address)
        found_records = True
        print(f"  IPv4 (A) 레코드 {len(ipv4_addresses)}개 발견.")
    except dns.resolver.NoAnswer:
        # 해당 타입의 레코드가 없을 경우 발생하는 예외
        print("  IPv4 (A) 레코드가 없습니다.")
        pass # A 레코드가 없더라도 AAAA 레코드를 시도해야 하므로 예외를 무시하고 진행
    except dns.resolver.NXDOMAIN:
        # 도메인 자체가 존재하지 않을 경우 발생하는 예외
        print(f"오류: 도메인 '{domain_to_lookup}'이 존재하지 않습니다 (NXDOMAIN).", file=sys.stderr)
        return ipv4_addresses # 도메인 오류를 알리기 위해 [] 리턴
    except Exception as e:
        # 그 외 DNS 조회 중 발생한 오류
        print(f"IPv4 레코드 조회 중 오류 발생: {e}", file=sys.stderr)
        # 오류 발생 시에도 AAAA 조사를 위해 계속 진행하거나 중단할 수 있습니다. 여기서는 계속 진행.
        pass

    return ipv4_addresses



if __name__ == "__main__":
    domain_to_lookup = input("조회할 도메인 이름을 입력하세요 (예: google.com): ")

    ipv4_ips = find_all_ips_for_domain(domain_to_lookup)
    ic(ipv4_ips)
    print(type(ipv4_ips))

    if ipv4_ips is not None:
        for ip in ipv4_ips:
            print(ip)
    
    '''
    ipv4_ips, ipv6_ips = get_all_ips_for_domain(domain_to_lookup)

    if ipv4_ips is not None: # 도메인이 유효했다면 (NXDOMAIN 오류가 아니었다면)
        print(f"\n---- 도메인 '{domain_to_lookup}'에 연결된 모든 IP 주소 ----")

        if ipv4_ips:
            print("  [IPv4 주소]:")
            for ip in ipv4_ips:
                print(f"    {ip}")
        else:
            print("  [IPv4 주소]: 없음")

        if ipv6_ips:
            print("  [IPv6 주소]:")
            for ip in ipv6_ips:
                print(f"    {ip}")
        else:
            print("  [IPv6 주소]: 없음")

        print("-------------------------------------------------")
    # 도메인 오류 (None, None 반환) 경우는 이미 함수 내에서 메시지 출력
    '''