import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2310139_2310090_2310191_2310242_2310423

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 100
# if __name__ == "__main__":
#     """Test a given policy on the Cutting Stock environment."""
#     num_episodes = NUM_EPISODES

    
#     policies = [GreedyPolicy(), RandomPolicy(), GeneticPolicy()]
#   # Ensure the same seed is used for all runs

#     # Run the test for each policy 3 times
#     for j, policy in enumerate(policies):
#         print(f"Testing {policy.__class__.__name__}")
#         for i in range(3):  # Three runs
#             print(f"  Run {i + 1} of 3")
#             observation, info = env.reset(seed = 42)

#             # Simulate for num_episodes
#             for ep in range(num_episodes):
#                 action = policy.get_action(observation, info)
#                 observation, reward, terminated, truncated, info = env.step(action)
#                 if terminated :
#                     print(f"Episode {ep + 1} terminated")
#                     break
#                 elif truncated:
#                     print(f"Episode {ep + 1} truncated")
#                     break

#             # Collect the final filled ratio for this run
#             print(info['filled_ratio'])

#     # Compute and print the average for each policy
  
#     env.close()

if __name__ == "__main__":
    observation, info = env.reset(seed=42)
    print(info)

    policy2210xxx = Policy2310139_2310090_2310191_2310242_2310423()
    for _ in range(200):
        action = policy2210xxx.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)
        print(info)

        if terminated or truncated:
            observation, info = env.reset()

    env.close()