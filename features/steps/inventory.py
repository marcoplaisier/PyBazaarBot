from mock import Mock
from agent import Agent
import logging


def before_all(context):
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

@given('the Agent')
def step_impl(context):
    Bazaar = Mock()
    context.agent = Agent(Bazaar())

@when('given {amount} {item}')
def step_impl(context, amount, item):
    context.agent.inventory[item] = int(amount)

@then('the Agent owns {amount} {item}')
def step_impl(context, amount, item):
    context.agent.inventory[item] == int(amount)

@given('the Agent has {amount} inventory space')
def step_impl(context, amount):
    Bazaar = Mock()
    context.agent = Agent(Bazaar(), inventory_space=int(amount))

@then('the Agent has {remaining} inventory space left')
def step_impl(context, remaining):
    assert context.agent.available_inventory_space == int(remaining)