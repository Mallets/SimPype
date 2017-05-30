import simpype
import random


sim = simpype.Simulation(id = 'test')
sim.seed = 42
sim.log.dir = '/tmp/log'
sim.model.dir = 'examples/model'
sim.log.property('items')
sim.log.property('priority')

# Gen00 -> Res00
gen00 = sim.add_generator(id = 'gen00')
gen00.random['arrival'] = {0: lambda: 1.0}
res00 = sim.add_resource(id = 'res00')
res00.random['service'] = {0: lambda: 1.0}
p00 = sim.add_pipeline(gen00, res00)

# Gen01 -> Res01
gen01 = sim.add_generator(id = 'gen01')
gen01.random['arrival'] = simpype.random.Random(sim, {0: lambda: 1.0})
res01 = sim.add_resource(id = 'res01')
res01.random['service'] = {0: lambda: 1.0}
p01 = sim.add_pipeline(gen01, res01)

# Gen02 -> Res02
gen02 = sim.add_generator(id = 'gen02')
gen02.random['initial'] = {0: lambda: 1.0}
gen02.random['arrival'] = {0: lambda: 1.0}
res02 = sim.add_resource(id = 'res02')
res02.random['service'] = {0: lambda: 1.0}
p02 = sim.add_pipeline(gen02, res02)

# Gen03 -> Res03
gen03 = sim.add_generator(id = 'gen03', model = 'r_generator')
gen03.random['arrival'] = {0: lambda: 1.0}
gen03.message.property['lifetime'] = {0: lambda: 10.0}
res03 = sim.add_resource(id = 'res03')
res03.random['service'] = {0: lambda: 1.0}
p03 = sim.add_pipeline(gen03, res03)

# Gen04 |-> Res04a
#       |-> Res04b
gen04 = sim.add_generator(id = 'gen04')
gen04.random['arrival'] = {0: lambda: 1.0}
gen04.message.property['lifetime'] = {0: lambda: 10.0}
res04a = sim.add_resource(id = 'res04a')
res04a.random['service'] = {0: lambda: 1.0}
res04b = sim.add_resource(id = 'res04b')
res04b.random['service'] = {0: lambda: 1.0}
p04a = sim.add_pipeline(gen04, res04a)
p04b = sim.add_pipeline(gen04, res04b)
p04 = sim.merge_pipeline(p04a, p04b)

# Gen05a |-> Res05
# Gen05b |
gen05a = sim.add_generator(id = 'gen05a')
gen05a.random['arrival'] = {0: lambda: 1.0}
gen05a.message.property['lifetime'] = {0: lambda: 2.0}
gen05b = sim.add_generator(id = 'gen05b')
gen05b.random['arrival'] = {0: lambda: 2.0}
res05 = sim.add_resource(id = 'res05')
p05a = sim.add_pipeline(gen05a, res05)
p05b = sim.add_pipeline(gen05b, res05)

@simpype.resource.service(res05)
def service(self, message):
	if 'lifetime' in message.property:
		yield self.env.timeout(5.0)
	else:
		yield self.env.timeout(1.0)

# Gen06 -> Res06
gen06 = sim.add_generator(id = 'gen06')
gen06.random['arrival'] = {0: lambda: 1.0}
gen06.message.property['items'] = {0: lambda: random.randint(0,10)}
res06 = sim.add_resource(id = 'res06', model = 'r_cashier')
res06.random['service'] = {0: lambda: 1.0}
p06 = sim.add_pipeline(gen06, res06)

# Gen07 -> Res07
gen07 = sim.add_generator(id = 'gen07')
gen07.random['arrival'] = {0: lambda: 1.0}
gen07.message.property['property'] = {0: lambda: random.randint(0,4)}
res07 = sim.add_resource(id = 'res07', pipe = 'p_priority')
res07.random['service'] = {0: lambda: 1.0}
p07 = sim.add_pipeline(gen07, res07)

# Gen08 -> Res08
gen08 = sim.add_generator(id = 'gen08')
gen08.random['arrival'] = {0: lambda: 1.0}
gen08.message.property['items'] = {1: lambda: 1}
res08 = sim.add_resource(id = 'res08')
res08.random['service'] = {0: lambda: 1.0}
p08 = sim.add_pipeline(gen08, res08)

# Gen09 -> Res09a |-> Res09b
#                 |-> Res09c -> Res09d
gen09 = sim.add_generator(id = 'gen09')
gen09.random['arrival'] = {0: lambda: 1.0}
res09a = sim.add_resource(id = 'res09a')
res09a.random['service'] = {0: lambda: 1.0}
res09b = sim.add_resource(id = 'res09b')
res09b.random['service'] = {0: lambda: 1.0}
res09c = sim.add_resource(id = 'res09c')
res09c.random['service'] = {0: lambda: 1.0}
res09d = sim.add_resource(id = 'res09d')
res09d.random['service'] = {0: lambda: 1.0}
p09a = sim.add_pipeline(gen09, res09a)
p09b = sim.add_pipeline(p09a, res09b)
p09c = sim.add_pipeline(res09c, res09d)
p09d = sim.add_pipeline(p09a, p09c)
p09 = sim.merge_pipeline(p09b, p09d)

@simpype.resource.service(res09a)
def service(self, message):
	if message.seq_num % 2 == 0:
		message.next = res09b
	else:
		message.next = p09c

# Gen10 -> Res10a -> Res10b -> Res10c
gen10 = sim.add_generator(id = 'gen10')
gen10.random['arrival'] = {0: lambda: 1.0}
res10a = sim.add_resource(id = 'res10a')
res10b = sim.add_resource(id = 'res10b')
res10c = sim.add_resource(id = 'res10c')
p10 = sim.add_pipeline(gen10, res10a, res10b, res10c)

e = sim.env.event()
def fcallback(message, value):
	global e
	message.timestamp('callback.' + str(value))

@simpype.resource.service(res10a)
def service(self, message):
	global e
	message.subscribe(event = e, callback = fcallback, id = 'event')
	yield self.env.timeout(1.0)

@simpype.resource.service(res10b)
def service(self, message):
	global e
	message.subscribe(event = e, callback = fcallback, id = 'event')
	yield self.env.timeout(1.0)

@simpype.resource.service(res10c)
def service(self, message):
	global e
	if 'event' in message.subscription:
		message.unsubscribe(id = 'event')
	yield self.env.timeout(1.0)

def clock():
	global e
	while True:
		yield sim.env.timeout(5.0)
		e.succeed('tick')
		e = sim.env.event()
sim.env.process(clock())

# Gen11 -> Res11
gen11 = sim.add_generator(id = 'gen11')
gen11.random['arrival'] = {0: lambda: 1.0}
gen11.message.property['priority'] = {0: lambda: random.randint(0,4)}
res11 = sim.add_resource(id = 'res11', pipe = 'p_priority')
res11.random['service'] = {0: lambda: 1.0}
p11 = sim.add_pipeline(gen11, res11)

# Gen12 -> Res12
gen12 = sim.add_generator(id = 'gen12')
gen12.random['arrival'] = {0: lambda: 1.0}
res12 = sim.add_resource(id = 'res12')
res12.random['service'] = {0: lambda: 1.0}
p12 = sim.add_pipeline(gen12, res12)

@simpype.pipe.enqueue(res12.pipe)
def enqueue(self, message):
	message.timestamp('pipe.enqueue.test.function')
	if message.seq_num % 2 == 0:
		message.drop('bad.luck')
	else:
		return self.queue['default'].push(message)

@simpype.pipe.dequeue(res12.pipe)
def dequeue(self):
	message = self.queue['default'].pop()
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.dequeue.test.function')
	return message

# Gen13 -> Res13
gen13 = sim.add_generator(id = 'gen13')
gen13.random['arrival'] = {0: lambda: 1.0}
res13 = sim.add_resource(id = 'res13')
res13.random['service'] = {0: lambda: 1.0}
p13 = sim.add_pipeline(gen13, res13)

@simpype.pipe.enqueue(res13.pipe)
def enqueue(self, message):
	yield self.env.timeout(0)
	message.timestamp('pipe.enqueue.test.generator')
	return self.queue['default'].push(message)

@simpype.pipe.dequeue(res13.pipe)
def dequeue(self):
	yield self.env.timeout(0)
	message = self.queue['default'].pop()
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.dequeue.test.generator')
	return message

# Gen14 -> Res14
gen14 = sim.add_generator(id = 'gen14')
gen14.random['arrival'] = {0: lambda: 1.0}
res14 = sim.add_resource(id = 'res14')
res14.random['service'] = {0: lambda: 2.0}
res14.pipe.queue['default'].capacity = 1
p14 = sim.add_pipeline(gen14, res14)

# Gen15 -> Res15
gen15 = sim.add_generator(id = 'gen15')
gen15.random['arrival'] = {0: lambda: 1.0}
res15 = sim.add_resource(id = 'res15')
res15.random['service'] = {0: lambda: 1.0}
p15 = sim.add_pipeline(gen15, res15)

@simpype.pipe.dequeue(res15.pipe)
def dequeue(self):
	message = self.queue['default'].pop()
	message = self.queue['default'].pop()
	return message

# Gen16 -> Res16
gen16 = sim.add_generator(id = 'gen16')
gen16.random['arrival'] = {0: lambda: 1.0}
res16 = sim.add_resource(id = 'res16')
res16.random['service'] = {0: lambda: 1.0}
p16 = sim.add_pipeline(gen16, res16)

@simpype.pipe.dequeue(res16.pipe.queue['default'])
def dequeue(self):
	message = self.queue['default'].pop()
	message = self.queue['default'].pop()
	return message

@simpype.queue.push(res16.pipe.queue['default'])
def push(self, message):
	self.buffer.append(message)
	message.timestamp('queue.push.test')

@simpype.queue.pop(res16.pipe.queue['default'])
def pop(self):
	if len(self.buffer) > 0:
		message = self.buffer.pop(0)
		message.timestamp('queue.push.test')
		return message
	else:
		return None
#
## Run until t=60
sim.run(until = 60)
