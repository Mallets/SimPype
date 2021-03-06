import simpype
import random

# Create simulation environment
sim = simpype.Simulation(id = 'test')
# Set the pseudo-random number generator seed
sim.seed = 42
# Set the log dir
sim.log.dir = '/tmp/log'
# Set the model directory
sim.model.dir = 'examples/model'
# Log custom message property
sim.log.property('items')

# Add generator 
gen00 = sim.add_generator(id = 'gen00')
# Set arrival time
gen00.random['arrival'] = {0: lambda: 1.0}

# Add resource
res00 = sim.add_resource(id = 'res00')
# Create random dictionary and set service time
res00.random['service'] = simpype.random.Random(sim, {0: lambda: 1.0})

# Add pipeline
p00 = sim.add_pipeline(gen00, res00)

# Add generator with custom model
gen02 = sim.add_generator(id = 'gen02', model = 'r_generator')
gen02.random['arrival'] = {
	0: lambda: 1.0,
	5: lambda: None
}
# Set message lifetime
res02 = sim.add_resource(id = 'res02')
res02.random['service'] = {0: lambda: 1.0}
p02 = sim.add_pipeline(gen02, res02)

# Add generator with custom model
gen03 = sim.add_generator(id = 'gen03', model = 'r_generator')
gen03.random['arrival'] = {0: lambda: 1.0}
# Set message lifetime
gen03.message.property['lifetime'] = {0: lambda: 10.0}
res03 = sim.add_resource(id = 'res03')
res03.random['service'] = {0: lambda: 1.0}
p03 = sim.add_pipeline(gen03, res03)

## Automatic copy of the message
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

# Lifetime expire
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
gen07.random['arrival'] = {
	2: lambda: 1.0,
	11: lambda: None,
	12: lambda: None,
	13: lambda: None,
	14: lambda: 1.0,
	45: lambda: None,
	56: lambda: None,
}
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
gen11a = sim.add_generator(id = 'first')
gen11a.random['arrival'] = {0: lambda: 5.0}
gen11b = sim.add_generator(id = 'business')
gen11b.random['arrival'] = {0: lambda: 2.0}
gen11c = sim.add_generator(id = 'economy')
gen11c.random['arrival'] = {0: lambda: 1.0}
res11 = sim.add_resource(id = 'res11', pipe = 'p_priority')
res11.random['service'] = {0: lambda: 1.0}
p11a = sim.add_pipeline(gen11a, res11)
p11b = sim.add_pipeline(gen11b, res11)
p11c = sim.add_pipeline(gen11c, res11)

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

@simpype.pipe.dequeue(res16.pipe)
def dequeue(self):
	message = self.queue['default'].pop()
	message = self.queue['default'].pop()
	return message

@simpype.queue.push(res16.pipe.queue['default'])
def push(self, message):
	self.disable()
	self.buffer.append(message)
	message.timestamp('queue.push.test')
	self.enable()
	return message

@simpype.queue.pop(res16.pipe.queue['default'])
def pop(self):
	if len(self.buffer) > 0:
		message = self.buffer.pop(0)
		message.timestamp('queue.push.test')
		return message
	else:
		return None

# Gen17 -> Res17
gen17 = sim.add_generator(id = 'gen17')
gen17.random['arrival'] = {0: lambda: 1.0}
gen17.message.property['size'] = {0: lambda: random.randint(1,20)}
gen17.message.property['priority'] = 0
res17 = sim.add_resource(id = 'res17', pipe = 'p_wfq')
res17.random['service'] = {0: lambda: 1.0}
res17.pipe.classes
res17.pipe.queue[0].capacity = 20
p17 = sim.add_pipeline(gen17, res17)

# Gen18 -> Res18
gen18 = sim.add_generator(id = 'gen18')
gen18.random['arrival'] = {0: lambda: 1.0}
gen18.message.property['size'] = {0: lambda: random.randint(1,20)}
res18 = sim.add_resource(id = 'res18', pipe = 'p_wfq')
res18.random['service'] = {0: lambda: 1.0}
p18 = sim.add_pipeline(gen18, res18)

@simpype.pipe.enqueue(res18.pipe)
def enqueue(self, message):
	self.queue[0].pop()
	self.queue[0].pop()
	self.queue[0].push(message)

# Gen19 -> Res19
gen19 = sim.add_generator(id = 'gen19')
gen19.random['arrival'] = {0: lambda: 1.0}
res19 = sim.add_resource(id = 'res19', pipe = 'p_wfq')
res19.random['service'] = {0: lambda: 1.0}
p19 = sim.add_pipeline(gen19, res19)

# Gen20a |-> Res20
# Gen20b |
gen20a = sim.add_generator(id = 'gen20a')
gen20a.random['arrival'] = {0: lambda: 2.0}
gen20a.message.property['priority'] = {0: lambda: random.randint(0,4)}
gen20b = sim.add_generator(id = 'gen20b')
gen20b.random['arrival'] = {0: lambda: 2.0}
res20 = sim.add_resource(id = 'res20', pipe = 'p_roundrobin')
res20.random['service'] = {0: lambda: 1.0}
p20a = sim.add_pipeline(gen20a, res20)
p20b = sim.add_pipeline(gen20b, res20)

# Gen21 |-> Res21
gen21 = sim.add_generator(id = 'gen21')
gen21.random['arrival'] = {0: lambda: 1.0}
gen21.message.log = False
res21 = sim.add_resource(id = 'res21')
p21 = sim.add_pipeline(gen21, res21)

# Gen22 |-> Res22
gen22 = sim.add_generator(id = 'gen22')
gen22.random['arrival'] = {0: lambda: 1.0}
res22 = sim.add_resource(id = 'res22')
res22.log = False
p22 = sim.add_pipeline(gen22, res22)

# Gen23 |-> Res23
gen23 = sim.add_generator(id = 'gen23')
gen23.random['arrival'] = {0: lambda: 1.0}
res23 = sim.add_resource(id = 'res23')
res23.pipe.log = False
p23 = sim.add_pipeline(gen23, res23)

# Gen24 |-> Res24
gen24 = sim.add_generator(id = 'gen24')
gen24.random['arrival'] = {0: lambda: 1.0}
res24 = sim.add_resource(id = 'res24')
res24.pipe.queue['default'].log = False
p24 = sim.add_pipeline(gen24, res24)

# Gen25 |-> Res25
gen25 = sim.add_generator(id = 'gen25')
gen25.random['arrival'] = {0: lambda: 1.0}
gen25.random['quantity'] = {0: lambda: random.randint(1,10)}
res25 = sim.add_resource(id = 'res25')
res25.random['service'] = {0: lambda: 1.0}
p25 = sim.add_pipeline(gen25, res25)

sim.log.file = True
sim.log.print = False
sim.run(until = 30)

sim.log.file = False
sim.log.print = True
sim.run(until = 60)

sim.log.file = True
sim.log.print = True
sim.run(until = 90)

sim.log.file = False
sim.log.print = False
sim.run(until = 120)
