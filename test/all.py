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
res03 = sim.add_resource(id = 'res03')
res03.random['service'] = {0: lambda: 1.0}
p03 = sim.add_pipeline(gen03, res03)

# Gen04 |-> Res04a
#       |-> Res04b
gen04 = sim.add_generator(id = 'gen04')
gen04.random['arrival'] = {0: lambda: 1.0}
res04a = sim.add_resource(id = 'res04a')
res04a.random['service'] = {0: lambda: 1.0}
res04b = sim.add_resource(id = 'res04b')
res04b.random['service'] = {0: lambda: 1.0}
p04a = sim.add_pipeline(gen04, res04a)
p04b = sim.add_pipeline(gen04, res04b)
p04 = sim.merge_pipeline(p04a, p04b)

# Gen05 -> Res05
gen05 = sim.add_generator(id = 'gen05')
gen05.random['arrival'] = {0: lambda: 1.0}
gen05.message.property['lifetime'] = {0: lambda: 1.0}
res05 = sim.add_resource(id = 'res05')
res05.random['service'] = {0: lambda: 2.0}
p05 = sim.add_pipeline(gen05, res05)

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
res07 = sim.add_resource(id = 'res07', pipe = 'r_priority')
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
res10b.random['service'] = {0: lambda: 1.0}
res10c = sim.add_resource(id = 'res10c')
p10 = sim.add_pipeline(gen10, res10a, res10b, res10c)

e = sim.env.event()
def fcallback(message, value):
	global e
	message.timestamp('callback.' + str(value))

@simpype.resource.service(res10a)
def service(self, message):
	global e
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e)
	message.subscribe(callback = fcallback, event = e, id = 'event')
	message.subscribe(callback = fcallback, event = e, id = 'event')
	yield sim.env.timeout(1.0)

@simpype.resource.service(res10c)
def service(self, message):
	global e
	if 'event' in message.subscription:
		message.unsubscribe('event')
	if e in message.subscription:
		message.unsubscribe(e)
	yield sim.env.timeout(1.0)

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
res11 = sim.add_resource(id = 'res11')
res11.random['service'] = {0: lambda: 1.0}
p11 = sim.add_pipeline(gen11, res11)

@simpype.pipe.enqueue(res11.pipe)
def enqueue(self, message):
	message.timestamp('pipe.enqueue.test')
	return self.queue['default'].push(message)

@simpype.pipe.dequeue(res11.pipe)
def dequeue(self):
	message = self.queue['default'].pop()
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.dequeue.test')
	return message

# Gen12 -> Res12
gen12 = sim.add_generator(id = 'gen12')
gen12.random['arrival'] = {0: lambda: 1.0}
gen12.message.property['priority'] = {0: lambda: random.randint(0,4)}
res12 = sim.add_resource(id = 'res12', pipe = 'p_priority')
res12.random['service'] = {0: lambda: 1.0}
p12 = sim.add_pipeline(gen12, res12)

#@simpype.pipe.enqueue(res12.pipe)
#def enqueue(self, message):
#	self.queue['default'].disable()
#	yield self.env.timeout(0)
#	message.timestamp('pipe.enqueue.test')
#	message = self.queue['default'].push(message)
#	if message.seq_num % 10 == 0:
#		message.drop('badluck')
#	self.queue['default'].enable()
#	return message
#
#@simpype.pipe.dequeue(res1.pipe)
#def dequeue(self):
#	yield self.env.timeout(0)
#	message = self.queue['default'].pop()
#	if isinstance(message, simpype.Message):
#		message.timestamp('pipe.dequeue.test')
#	return message
#
#
#@simpype.pipe.enqueue(res6.pipe)
#def enqueue(self, message):
#	message.timestamp('pipe.enqueue.test')
#	return self.queue['default'].push(message)
#
#@simpype.pipe.dequeue(res6.pipe)
#def dequeue(self):
#	message = self.queue['default'].pop()
#	if isinstance(message, simpype.Message):
#		message.timestamp('pipe.dequeue.test')
#	return message
#
#@simpype.queue.push(res7.pipe.queue['default'])
#def push(self, message):
#	self.buffer.append(message)
#	message.timestamp('queue.push.test')
#
#@simpype.queue.pop(res7.pipe.queue['default'])
#def pop(self):
#	if len(self.buffer) > 0:
#		message = self.buffer.pop(0)
#		message.timestamp('queue.push.test')
#		return message
#	else:
#		return None
#
## Run until t=60
sim.run(until = 60)
