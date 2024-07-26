import numpy as np

# TODO: if the last pool doesn't add up to more than h, move all agents to a pool with >= h randomly
# Bin cover using 2/3 approximation in O(nlogn)
def bin_cover_approx(agents):
    n = len(agents)
    threshold_value = agents[0].threshold_value
    agents.sort(key=lambda agent: agent.stake, reverse=True)

    # agent.id=i ^ agent.pool=i -> agent with ID=i opens a pool
    # agent.id=i ^ agent.pool=j, i!=j -> agent with ID=i has their stake at pool of agent j

    max_ptr = 0
    min_ptr = n-1
    curr_sum = 0
    curr_pool = 0
    total_pools = 0

    while max_ptr <= min_ptr:
        if curr_sum == 0:
            total_pools += 1
            curr_sum = agents[max_ptr].stake
            curr_pool = agents[max_ptr].id
            agents[max_ptr].take_action(curr_pool)
            max_ptr += 1
        elif curr_sum + agents[max_ptr].stake < threshold_value:
            curr_sum += agents[max_ptr].stake
            agents[max_ptr].take_action(curr_pool)
            max_ptr += 1
        else:
            while max_ptr <= min_ptr and curr_sum < threshold_value:
                agents[min_ptr].take_action(curr_pool)
                curr_sum += agents[min_ptr].stake
                min_ptr -= 1
            curr_sum = 0

    agents.sort(key=lambda agent: agent.id)
    if curr_sum < threshold_value:
        agents_to_move = np.where(np.array([agent.pool for agent in agents]) == curr_pool)[0]
        pools = np.array([agent.pool for i, agent in enumerate(agents) if i == agent.pool])
        pools = np.delete(pools, np.where(pools == curr_pool))
        for agent_id in agents_to_move:
            agents[agent_id].take_action(np.random.choice(pools))
        total_pools -= 1

    return np.array(agents), total_pools