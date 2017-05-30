import simpype
import random


sim = simpype.Simulation(id = 'test')
sim.seed = 42
sim.log.dir = '/tmp/log'
sim.model.dir = 'examples/model'

sim.log.property('items')

gen0 = sim.add_generator(id = 'gen0')
gen0.random['initial'] = {
	0	: lambda: 1.0
}
gen0.random['arrival'] = simpype.random.Random(sim, {
	0.1	: lambda: 1.0,
	10	: lambda: random.uniform(0.5, 1.5),
	20	: lambda: random.expovariate(1.0)
})
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
p2a = sim.add_pipeline(p0, res2)
p2b = sim.add_pipeline(p1, res2)
p3a = sim.add_pipeline(p0, res3)
p3b = sim.add_pipeline(p1, res3)
p4 = sim.add_pipeline(res3, res4)
p6 = sim.add_pipeline(res5, res6)
p8 = sim.add_pipeline(res7, res8)
p7 = sim.add_pipeline(res5, p8)
p5a = sim.add_pipeline(res3, p7)
p5b = sim.add_pipeline(res3, p6)
pM = sim.merge_pipeline(p0, p1, p2a, p2b, p3a, p3b, p4, p5a, p5b, p6, p7)


e = sim.env.event()
def fcallback(message, value):
	global e
	message.timestamp('callback')	
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e, id = 'event')
	message.subscribe(callback = fcallback, event = e, id = 'event')

res1.pipe.debug = True
@simpype.pipe.enqueue(res1.pipe)
def enqueue(self, message):
	self.queue['default'].disable()
	yield self.env.timeout(0)
	message.timestamp('pipe.enqueue.test')
	message = self.queue['default'].push(message)
	if message.seq_num % 10 == 0:
		message.drop('badluck')
	self.queue['default'].enable()
	return message

@simpype.pipe.dequeue(res1.pipe)
def dequeue(self):
	yield self.env.timeout(0)
	message = self.queue['default'].pop()
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.dequeue.test')
	return message

@simpype.queue.push(res2.pipe.queue['default'])
def push(self, message):
	self.buffer.append(message)
	message.timestamp('queue.push.test')

@simpype.queue.pop(res2.pipe.queue['default'])
def pop(self):
	if len(self.buffer) > 0:
		message = self.buffer.pop(0)
		message.timestamp('queue.push.test')
		return message
	else:
		return None

@simpype.resource.service(res3)
def service(self, message):
	global e
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e, id = 'event')
	message.subscribe(callback = fcallback, event = e, id = 'event')
	if message.seq_num % 10 == 0:
		message.drop('badluck')

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

@simpype.pipe.enqueue(res6.pipe)
def enqueue(self, message):
	message.timestamp('pipe.enqueue.test')
	return self.queue['default'].push(message)

@simpype.pipe.dequeue(res6.pipe)
def dequeue(self):
	message = self.queue['default'].pop()
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.dequeue.test')
	return message

@simpype.resource.service(res7)
def service(self, message):
	global e
	message.subscribe(callback = fcallback, event = e, id = 'event')
	if 'lifetime' in message.property:
		message.unsubscribe('lifetime')

# Run until t=30
sim.run(until = 30)
