import simpype
import random


sim = simpype.Simulation(id = 'test')
sim.seed = 42
sim.log.dir = '/tmp/log'
sim.model.dir = 'examples/model'

gen0 = sim.add_generator(id = 'gen0')
gen0.random['initial'] = {
	0	: lambda: 1.0
}
gen0.random['arrival'] = {
	0	: lambda: 1.0,
	10	: lambda: random.uniform(0.5, 1.5),
	20	: lambda: random.expovariate(1.0)
}
gen0.message.property['items'] = {
	0	: lambda: random.randint(0, 10),
}

gen1 = sim.add_generator(id = 'gen1')
gen1.random['initial'] = {
	0	: lambda: 1.0
}
gen1.random['arrival'] = {
	0	: lambda: 1.0,
	10	: lambda: random.uniform(0.5, 1.5),
	20	: lambda: random.expovariate(1.0)
}
gen1.message.property['lifetime'] = {
	0	: lambda: 1.0,
	10	: lambda: random.uniform(0.5, 1.5),
	20	: lambda: random.expovariate(1.0)
}
gen1.message.property['items'] = {
	0	: lambda: random.randint(0, 10),
}

res0 = sim.add_resource(id = 'res0')
res0.random['service'] = {
	0	: lambda: 0.5,
	10	: lambda: random.uniform(0.25, 0.75),
	20	: lambda: random.expovariate(0.5)
}

res1 = sim.add_resource(id = 'res1')
res1.random['service'] = {
	0	: lambda: 0.25,
	10	: lambda: random.uniform(0.10, 0.50),
	20	: lambda: random.expovariate(0.25)
}

res2 = sim.add_resource(id = 'res2')
res3 = sim.add_resource(id = 'res3')
res4 = sim.add_resource(id = 'res4')
res5 = sim.add_resource(id = 'res5')
res6 = sim.add_resource(id = 'res6')
res6.random['service'] = {
	0	: lambda: 5.0,
}
res7 = sim.add_resource(id = 'res7')
res7.random['service'] = {
	0	: lambda: 5.0,
}
res8 = sim.add_resource(id = 'res8', model = 'cashier')

p0 = sim.add_pipeline(gen0, res0, res1)
p1 = sim.add_pipeline(gen1, res1)
p2 = sim.add_pipeline(res1, res2)
p3 = sim.add_pipeline(res1, res3)
p4 = sim.add_pipeline(res3, res4)
p6 = sim.add_pipeline(res5, res6)
p8 = sim.add_pipeline(res7, res8)
p7 = sim.add_pipeline(res5, p8)
p5a = sim.add_pipeline(res3, p7)
p5b = sim.add_pipeline(res3, p6)
pM = sim.merge_pipeline(p0, p1, p2, p3, p4, p5a, p5b, p6, p7)


e = sim.env.event()

def fcallback(message, value):
	global e
	message.timestamp('callback')	
	message.subscribe(callback = fcallback, event = e)

@simpype.resource.service(res3)
def service(self, message):
	global e
	message.subscribe(callback = fcallback, event = e, id = 'event')

@simpype.resource.service(res5)
def service(self, message):
	global e
	if message.seq_num % 2 == 0:
		message.next = res6
	else:
		message.next = p8
	if message.seq_num % 5 == 0:
		e.succeed()
		e = sim.env.event()

@simpype.resource.service(res7)
def service(self, message):
	if 'lifetime' in message.property:
		message.unsubscribe('lifetime')

# Run until t=30
sim.run(until = 30)
