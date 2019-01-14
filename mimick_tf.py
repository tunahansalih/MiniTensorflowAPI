import tf_api as tf

graph = tf.Graph()
graph.as_default()

a = tf.Constant(15)
b = tf.Constant(10)

prod = tf.multiply(a,b)
sum = tf.add(a,b)

res = tf.divide(prod, sum)

session = tf.Session()

out = session.run(res)

print(out)









    
