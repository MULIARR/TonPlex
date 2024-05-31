import asyncio


class AtomicManager:
    def __init__(self):
        self.lock_dict: dict[str, asyncio.Lock] = {}

    async def get_or_create_lock(self, lock_key: str) -> asyncio.Lock:
        """
        Retrieves or creates an asyncio lock based on the given key to ensure
        atomic operations.

        Args:
            lock_key (str): A unique identifier for the lock.

        Returns:
            asyncio.Lock: The lock associated with `lock_key`.

        Example:
            key = f'{user_id}_{operation}'

            if key in atomic_manager.lock_dict: return

            lock = await atomic_manager.get_or_create_lock(key)

            async with lock:
                # Perform atomic operation
        """

        if lock_key not in self.lock_dict:
            self.lock_dict[lock_key] = asyncio.Lock()

        return self.lock_dict[lock_key]

    def release_lock(self, lock_key: str):
        """Function to remove the lock key"""

        del self.lock_dict[lock_key]


atomic_manager = AtomicManager()
