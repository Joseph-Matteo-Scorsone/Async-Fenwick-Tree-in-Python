import asyncio

class AsyncFenwickTreeRollingWindow:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)
        self.window = [0] * size
        self.current_index = 0

    async def _update_tree(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    async def _query_tree(self, index):
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total
    
    async def update(self, value):
        rolling_index = self.current_index % self.size
        fenwick_index = rolling_index + 1

        old_value = self.window[rolling_index]
        delta = value - old_value
        await self._update_tree(fenwick_index, delta)

        self.window[rolling_index] = value
        self.current_index += 1

    async def query(self, index):
        if index < 0 or index >= self.size:
            return "Invalid index"
        
        return self.tree[index]
    
    async def sum(self, index=None):
        if index == None:
            return await self._query_tree(self.size)
        else:
            return await self._query_tree(index)
        
    def to_string(self):
        return f"Window: {self.window}"

async def main():
    window_size = 5
    fenwick_tree = AsyncFenwickTreeRollingWindow(window_size)

    values = [10, 20, 30, 40, 50, 60, 70]
    for value in values:
        await fenwick_tree.update(value)
        print(f"Added {value}, current window Sum: {await fenwick_tree.sum()}, {fenwick_tree.to_string()} ")

    print(f"Query index 3: {await fenwick_tree.query(3)}")
    print(f"Sum to index 2: {await fenwick_tree.sum(2)}")

    ma = await fenwick_tree.sum() / fenwick_tree.size
    print(f"MA: {ma}")

asyncio.run(main())