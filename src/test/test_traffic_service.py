from service.traffic_service import TrafficService


class TestWebsite(object):
    if __name__ == "__main__":
        service = TrafficService()
        domain_name = "outofmemory.cn"
        bank = service.get_traffic(domain_name=domain_name)
        print(bank.reach_rank[0])
        print(bank.popularity_rank)
